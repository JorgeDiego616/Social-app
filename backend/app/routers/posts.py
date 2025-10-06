from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

router = APIRouter()

# ====== MODELOS ======
class PostBase(BaseModel):
    author_id: int = Field(..., description="ID del usuario autor")
    content: str = Field(..., min_length=1, max_length=500)

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1, max_length=500)

class PostOut(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime

# ====== DATA EN MEMORIA ======
_posts: List[PostOut] = []
_next_id = 1

def _get_next_id() -> int:
    global _next_id
    nid = _next_id
    _next_id += 1
    return nid

# ====== ENDPOINTS ======
@router.get("", response_model=List[PostOut])
def list_posts(author_id: Optional[int] = None):
    if author_id is not None:
        return [p for p in _posts if p.author_id == author_id]
    return _posts

@router.post("", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(payload: PostCreate):
    now = datetime.utcnow()
    new_post = PostOut(
        id=_get_next_id(),
        author_id=payload.author_id,
        content=payload.content,
        created_at=now,
        updated_at=now,
    )
    _posts.append(new_post)
    return new_post

@router.get("/{post_id}", response_model=PostOut)
def get_post(post_id: int):
    for p in _posts:
        if p.id == post_id:
            return p
    raise HTTPException(status_code=404, detail="Post not found")

@router.put("/{post_id}", response_model=PostOut)
def update_post(post_id: int, payload: PostUpdate):
    for i, p in enumerate(_posts):
        if p.id == post_id:
            data = payload.model_dump(exclude_unset=True)
            updated = p.model_copy(update={
                **data,
                "updated_at": datetime.utcnow()
            })
            _posts[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Post not found")

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    for i, p in enumerate(_posts):
        if p.id == post_id:
            _posts.pop(i)
            return
    raise HTTPException(status_code=404, detail="Post not found")
