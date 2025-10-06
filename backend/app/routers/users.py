from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List, Optional

router = APIRouter()

# ====== MODELOS ======
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str  # solo para ejemplo; NO guardes así en producción

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None

class UserOut(UserBase):
    id: int

# ====== DATA EN MEMORIA (se reinicia al apagar el server) ======
_users: List[UserOut] = []
_next_id = 1

def _get_next_id() -> int:
    global _next_id
    nid = _next_id
    _next_id += 1
    return nid

# ====== ENDPOINTS ======
@router.get("", response_model=List[UserOut])
def list_users():
    return _users

@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    # validación simple de email único
    if any(u.email == user.email for u in _users):
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = UserOut(
        id=_get_next_id(),
        username=user.username,
        email=user.email,
        full_name=user.full_name,
    )
    _users.append(new_user)
    return new_user

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    for u in _users:
        if u.id == user_id:
            return u
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate):
    for i, u in enumerate(_users):
        if u.id == user_id:
            updated = u.model_copy(update=payload.model_dump(exclude_unset=True))
            _users[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    for i, u in enumerate(_users):
        if u.id == user_id:
            _users.pop(i)
            return
    raise HTTPException(status_code=404, detail="User not found")
