from fastapi import FastAPI

# Aplicacion creada
app = FastAPI(title="Social App API", version="0.1.0")

# Ruta para probar
@app.get("/health")
def health():
    return {"status": "ok"}
