from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models import Base
import os

# ========================================
# 1. CREAR LA APLICACIÓN
# ========================================
app = FastAPI(
    title="API de Vehículos", 
    version="1.0",
    redirect_slashes=False  # ✅ Ahora sí está bien ubicado
)

# ========================================
# 2. CONFIGURAR CORS (ANTES DE TODO)
# ========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",  # Puerto por defecto de Angular
        "http://localhost:4400"   # ✅ Tu puerto actual según el error
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================================
# 3. CONFIGURAR TEMPLATES
# ========================================
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# ========================================
# 4. CREAR TABLAS EN LA BASE DE DATOS
# ========================================
Base.metadata.create_all(bind=engine)

# ========================================
# 5. IMPORTAR E INCLUIR ROUTERS
# ========================================
from app.routers import vehiculos, mecanicos, asignaciones, excel

app.include_router(vehiculos.router)
app.include_router(mecanicos.router)
app.include_router(asignaciones.router)  
app.include_router(excel.router)

# ========================================
# 6. RUTA DE INICIO (UNA SOLA)
# ========================================
@app.get("/")
def root():
    return {
        "mensaje": "API Taller Mecánico funcionando correctamente ✅",
        "endpoints": {
            "vehiculos": "/vehiculos",
            "mecanicos": "/mecanicos",
            "asignaciones": "/asignaciones",
            "excel": "/excel/upload",
            "docs": "/docs"
        }
    }