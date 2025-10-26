from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient

from app.routers import users, posts

# ==========================================
# CONFIGURACIÓN PRINCIPAL DE LA APLICACIÓN
# ==========================================
app = FastAPI(
    title="Social App API",
    version="0.1.0",
    description="Backend de la aplicación Social-APP conectada a MongoDB local."
)

# Servir los archivos del frontend
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")

# ==========================================
# CORS (Permitir peticiones desde el frontend)
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, cambia esto a los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# CONEXIÓN A MONGODB LOCAL
# ==========================================
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Social-APP"]  # Nombre de tu base de datos en MongoDB Compass
    print("✅ Conexión exitosa a MongoDB (localhost:27017)")
except Exception as e:
    print(f"❌ Error al conectar con MongoDB: {e}")
    db = None

# ==========================================
# ENDPOINT DE PRUEBA PARA CONEXIÓN A MONGO
# ==========================================
@app.get("/dbcheck")
def db_check():
    if not db:
        return {"status": "❌ No conectado a MongoDB"}
    try:
        colecciones = db.list_collection_names()
        return {
            "status": "✅ Conectado a MongoDB local",
            "database": "Social-APP",
            "colecciones": colecciones
        }
    except Exception as e:
        return {"status": "❌ Error al listar colecciones", "detalle": str(e)}

# ==========================================
# HEALTH CHECK
# ==========================================
@app.get("/health")
def health():
    return {"status": "ok"}

# ==========================================
# RUTAS (ROUTERS)
# ==========================================
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
