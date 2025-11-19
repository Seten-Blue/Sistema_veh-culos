from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Mecanico
from app.schemas import MecanicoCreate, MecanicoResponse
from typing import List

router = APIRouter(prefix="/mecanicos", tags=["Mecánicos"])

# Dependencia para DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[MecanicoResponse])
def obtener_mecanicos(db: Session = Depends(get_db)):
    return db.query(Mecanico).all()

@router.post("/", response_model=MecanicoResponse)
def crear_mecanico(m: MecanicoCreate, db: Session = Depends(get_db)):
    nuevo = Mecanico(**m.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
