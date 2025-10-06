from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI(title="Social Network API")

def get_db():
    conn = sqlite3.connect("social_network.db")
    conn.row_factory = sqlite3.Row
    return conn

# -------- USERS --------
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

@app.post("/users")
def create_user(user: dict):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, role) VALUES (?, ?) RETURNING *",
                (user["username"], user.get("role", "user")))
    new_user = dict(cur.fetchone())
    conn.commit()
    conn.close()
    return new_user

# -------- POSTS --------
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

@app.post("/posts")
def create_post(post: dict):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO posts (title, body, user_id) VALUES (?, ?, ?) RETURNING *",
                (post["title"], post["body"], post["user_id"]))
    new_post = dict(cur.fetchone())
    conn.commit()
    conn.close()
    return new_post

# -------- FOLLOWS --------
@app.post("/follow")
def follow_user(data: dict):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO follows (following_user_id, followed_user_id) VALUES (?, ?)",
                (data["following_user_id"], data["followed_user_id"]))
    conn.commit()
    conn.close()
    return {"message": "Now following!"}

@app.delete("/unfollow")
def unfollow_user(data: dict):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM follows WHERE following_user_id = ? AND followed_user_id = ?",
                (data["following_user_id"], data["followed_user_id"]))
    conn.commit()
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
