from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="Social Network API", version="2.0")

# ---------- CONFIGURACIÓN DE CORS ----------

app.add_middleware(
CORSMiddleware,
allow_origins=["*"],  # puedes cambiar a ["http://localhost:3000"]
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

# ---------- CONEXIÓN A BASE DE DATOS ----------

def get_db():
    conn = sqlite3.connect("social_network.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------- MODELOS Pydantic ----------

class UserCreate(BaseModel):
    username: str
    role: str = "user"

class PostCreate(BaseModel):
    title: str
    body: str
    user_id: int

class FollowAction(BaseModel):
    following_user_id: int
    followed_user_id: int

# ---------- USERS ----------

@app.get("/users")
def get_users():
    conn = get_db()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return [dict(u) for u in users]

@app.get("/users/{user_id}")
def get_user(user_id: int):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        return dict(user)

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, role) VALUES (?, ?)", (user.username, user.role))
        conn.commit()
        user_id = cur.lastrowid
        new_user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        conn.close()
        return dict(new_user)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Integrity error occurred while creating user.")
    

# ---------- POSTS ----------

@app.get("/posts")
def get_posts():
    conn = get_db()
    posts = conn.execute("""
    SELECT p.*, u.username
    FROM posts p
    JOIN users u ON p.user_id = u.id
    ORDER BY p.created_at DESC
    """).fetchall()
    conn.close()
    return [dict(p) for p in posts]

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
        "INSERT INTO posts (title, body, user_id) VALUES (?, ?, ?)",
        (post.title, post.body, post.user_id)
        )
        conn.commit()
        post_id = cur.lastrowid
        new_post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
        conn.close()
        return dict(new_post)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Invalid user_id")

# ---------- FOLLOWS ----------

@app.post("/follow", status_code=status.HTTP_201_CREATED)
def follow_user(data: FollowAction):
    if data.following_user_id == data.followed_user_id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
        "INSERT INTO follows (following_user_id, followed_user_id) VALUES (?, ?)",
        (data.following_user_id, data.followed_user_id)
        )
        conn.commit()
        conn.close()
        return {"message": "Now following!"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Already following or invalid users")

@app.delete("/unfollow")
def unfollow_user(data: FollowAction):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
    "DELETE FROM follows WHERE following_user_id = ? AND followed_user_id = ?",
    (data.following_user_id, data.followed_user_id)
    )
    conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Follow relationship not found")
    conn.close()
    return {"message": "Unfollowed successfully!"}

@app.get("/users/{user_id}/followers")
def get_followers(user_id: int):
    conn = get_db()
    rows = conn.execute("""
    SELECT u.id, u.username
    FROM follows f
    JOIN users u ON f.following_user_id = u.id
    WHERE f.followed_user_id = ?
    """, (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/users/{user_id}/following")
def get_following(user_id: int):
    conn = get_db()
    rows = conn.execute("""
    SELECT u.id, u.username
    FROM follows f
    JOIN users u ON f.followed_user_id = u.id
    WHERE f.following_user_id = ?
    """, (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API running and connected to backend"}
