from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="Social Network API", version="2.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "social_network.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    with open("schema.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

# ----- Pydantic -----
class UserCreate(BaseModel):
    username: str
    role: str = "user"

class PostCreate(BaseModel):
    title: str
    body: str
    user_id: int

class CommentCreate(BaseModel):
    post_id: int
    user_id: int
    text: str

class FollowAction(BaseModel):
    following_user_id: int
    followed_user_id: int

# ----- Users -----
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
    return dict(user)  # <-- corregido

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
        raise HTTPException(status_code=400, detail="Username already exists")

# ----- Posts -----
@app.get("/posts")
def get_posts():
    conn = get_db()
    posts = conn.execute("""
        SELECT p.*, u.username,
               (SELECT COUNT(*) FROM likes l WHERE l.post_id = p.id) AS like_count,
               (SELECT COUNT(*) FROM comments c WHERE c.post_id = p.id) AS comment_count
        FROM posts p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.created_at DESC
    """).fetchall()
    conn.close()
    return [dict(p) for p in posts]

@app.get("/posts/{post_id}")
def get_post(post_id: int):
    conn = get_db()
    post = conn.execute("""
        SELECT p.*, u.username
        FROM posts p JOIN users u ON p.user_id = u.id
        WHERE p.id = ?
    """, (post_id,)).fetchone()
    if not post:
        conn.close()
        raise HTTPException(status_code=404, detail="Post not found")
    comments = conn.execute("""
        SELECT c.*, u.username
        FROM comments c JOIN users u ON c.user_id = u.id
        WHERE c.post_id = ?
        ORDER BY c.created_at ASC
    """, (post_id,)).fetchall()
    like_count = conn.execute("SELECT COUNT(*) AS n FROM likes WHERE post_id = ?", (post_id,)).fetchone()["n"]
    conn.close()
    d = dict(post)
    d["comments"] = [dict(c) for c in comments]
    d["like_count"] = like_count
    return d

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO posts (title, body, user_id) VALUES (?, ?, ?)",
                    (post.title, post.body, post.user_id))
        conn.commit()
        post_id = cur.lastrowid
        new_post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
        conn.close()
        return dict(new_post)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Invalid user_id")

# ----- Likes -----
@app.post("/posts/{post_id}/like", status_code=status.HTTP_201_CREATED)
def like_post(post_id: int, user_id: int):
    try:
        conn = get_db()
        conn.execute("INSERT INTO likes (user_id, post_id) VALUES (?, ?)", (user_id, post_id))
        conn.commit()
        conn.close()
        return {"message": "Liked"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Already liked or invalid ids")

@app.delete("/posts/{post_id}/like")
def unlike_post(post_id: int, user_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM likes WHERE user_id = ? AND post_id = ?", (user_id, post_id))
    conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Like not found")
    conn.close()
    return {"message": "Unliked"}

# ----- Comments -----
@app.post("/comments", status_code=status.HTTP_201_CREATED)
def add_comment(c: CommentCreate):
    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO comments (post_id, user_id, text) VALUES (?, ?, ?)",
                    (c.post_id, c.user_id, c.text))
        conn.commit()
        comment_id = cur.lastrowid
        row = conn.execute("SELECT * FROM comments WHERE id = ?", (comment_id,)).fetchone()
        return dict(row)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Invalid post_id or user_id")
    finally:
        conn.close()

# ----- Follows -----
@app.post("/follow", status_code=status.HTTP_201_CREATED)
def follow_user(data: FollowAction):
    if data.following_user_id == data.followed_user_id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    try:
        conn = get_db()
        conn.execute(
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

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Inicializa tablas al arrancar
init_db()
