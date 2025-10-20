##import-Module .venv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, posts
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Social App API", version="0.1.0")
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en prod, restringe dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

# Rutas
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])


