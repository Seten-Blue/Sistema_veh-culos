from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Vehiculo
from app.schemas import VehiculoCreate, VehiculoResponse
from typing import List

router = APIRouter(prefix="/vehiculos", tags=["Vehículos"])

# Dependencia para DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ AMBAS RUTAS: con y sin barra final
@router.get("", response_model=List[VehiculoResponse])
@router.get("/", response_model=List[VehiculoResponse])
def obtener_vehiculos(db: Session = Depends(get_db)):
    """Obtiene todos los vehículos"""
    try:
        vehiculos = db.query(Vehiculo).all()
        print(f"✅ Listados {len(vehiculos)} vehículos")
        return vehiculos
    except Exception as e:
        print(f"❌ Error al obtener vehículos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al obtener vehículos: {str(e)}")

@router.post("", response_model=VehiculoResponse)
@router.post("/", response_model=VehiculoResponse)
def crear_vehiculo(v: VehiculoCreate, db: Session = Depends(get_db)):
    """Crea un nuevo vehículo"""
    try:
        nuevo = Vehiculo(**v.dict())
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        print(f"✅ Vehículo creado: {nuevo.marca} {nuevo.modelo}")
        return nuevo
    except Exception as e:
        db.rollback()
        print(f"❌ Error al crear vehículo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al crear vehículo: {str(e)}")