from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import SessionLocal
from app.models import Asignacion, Vehiculo, Mecanico
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

# ========================
# ROUTER
# ========================
router = APIRouter(
    prefix="/asignaciones",
    tags=["Asignaciones"]
)

# ========================
# SCHEMAS
# ========================
class AsignacionCreate(BaseModel):
    id_mecanico: int
    id_vehiculo: int
    descripcion: Optional[str] = ""
    estado: Optional[str] = "pendiente"

class AsignacionResponse(BaseModel):
    id: int
    id_mecanico: int
    id_vehiculo: int
    vehiculo: str
    mecanico: str
    descripcion: str
    fecha_asignacion: Optional[datetime]
    estado: str

    class Config:
        orm_mode = True

class ActualizacionEstado(BaseModel):
    estado: Optional[str] = None
    descripcion: Optional[str] = None

# ========================
# DEPENDENCIA DB
# ========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ========================
# MAPEO DE ESTADOS
# ========================
ESTADOS_MAP = {
    "Pendiente": "pendiente",
    "En Proceso": "en_proceso",
    "Completado": "completado",
    "pendiente": "pendiente",
    "en_proceso": "en_proceso",
    "completado": "completado"
}

ESTADOS_INVERSO = {
    "pendiente": "Pendiente",
    "en_proceso": "En Proceso",
    "completado": "Completado"
}

# ========================
# ENDPOINTS
# ========================

@router.get("/", response_model=List[AsignacionResponse])
def listar_asignaciones(db: Session = Depends(get_db)):
    """Listar todas las asignaciones"""
    try:
        asignaciones = db.query(Asignacion).options(
            joinedload(Asignacion.vehiculo),
            joinedload(Asignacion.mecanico)
        ).all()

        resultado = []
        for a in asignaciones:
            estado_frontend = ESTADOS_INVERSO.get(a.estado or "pendiente", "Pendiente")
            
            resultado.append({
                "id": a.id,
                "id_mecanico": a.id_mecanico or 0,
                "id_vehiculo": a.id_vehiculo or 0,
                "vehiculo": f"{a.vehiculo.marca} {a.vehiculo.modelo}" if a.vehiculo else "Sin información",
                "mecanico": f"{a.mecanico.nombre} {a.mecanico.apellido}" if a.mecanico else "Sin información",
                "descripcion": a.descripcion or "",
                "fecha_asignacion": a.fecha_asignacion,
                "estado": estado_frontend
            })

        print(f"✅ Listadas {len(resultado)} asignaciones")
        return resultado

    except Exception as e:
        print(f"❌ Error listando: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=AsignacionResponse)
def crear_asignacion(asignacion: AsignacionCreate, db: Session = Depends(get_db)):
    """Crear una nueva asignación"""
    try:
        mecanico = db.query(Mecanico).filter(Mecanico.id == asignacion.id_mecanico).first()
        vehiculo = db.query(Vehiculo).filter(Vehiculo.id == asignacion.id_vehiculo).first()

        if not mecanico:
            raise HTTPException(status_code=404, detail=f"Mecánico {asignacion.id_mecanico} no encontrado")
        if not vehiculo:
            raise HTTPException(status_code=404, detail=f"Vehículo {asignacion.id_vehiculo} no encontrado")

        estado_db = ESTADOS_MAP.get(asignacion.estado, "pendiente")
        
        nueva = Asignacion(
            id_mecanico=asignacion.id_mecanico,
            id_vehiculo=asignacion.id_vehiculo,
            descripcion=asignacion.descripcion or "",
            estado=estado_db
        )
        
        db.add(nueva)
        db.commit()
        db.refresh(nueva)

        print(f"✅ Asignación {nueva.id} creada")
        
        return AsignacionResponse(
            id=nueva.id,
            id_mecanico=nueva.id_mecanico,
            id_vehiculo=nueva.id_vehiculo,
            vehiculo=f"{vehiculo.marca} {vehiculo.modelo}",
            mecanico=f"{mecanico.nombre} {mecanico.apellido}",
            descripcion=nueva.descripcion or "",
            fecha_asignacion=nueva.fecha_asignacion,
            estado=ESTADOS_INVERSO.get(nueva.estado, "Pendiente")
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Error creando: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{asignacion_id}")
def actualizar_asignacion(
    asignacion_id: int,
    datos: ActualizacionEstado,
    db: Session = Depends(get_db)
):
    """Actualizar estado o descripción de una asignación"""
    try:
        print(f"🔄 PATCH asignación {asignacion_id}: {datos}")
        
        asignacion = db.query(Asignacion).filter(Asignacion.id == asignacion_id).first()
        
        if not asignacion:
            print(f"❌ Asignación {asignacion_id} no existe")
            raise HTTPException(status_code=404, detail=f"Asignación {asignacion_id} no encontrada")
        
        if datos.estado:
            estado_db = ESTADOS_MAP.get(datos.estado, "pendiente")
            asignacion.estado = estado_db
            print(f"   ✅ Estado → {estado_db}")
        
        if datos.descripcion is not None:
            asignacion.descripcion = datos.descripcion
            print(f"   ✅ Descripción actualizada")
        
        db.commit()
        db.refresh(asignacion)
        
        print(f"✅ Asignación {asignacion_id} actualizada")
        
        return {
            "mensaje": "Asignación actualizada",
            "id": asignacion.id,
            "estado": ESTADOS_INVERSO.get(asignacion.estado, "Pendiente"),
            "descripcion": asignacion.descripcion
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Error actualizando: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{asignacion_id}")
def eliminar_asignacion(asignacion_id: int, db: Session = Depends(get_db)):
    """Eliminar una asignación"""
    try:
        print(f"🗑️ DELETE asignación {asignacion_id}")
        
        asignacion = db.query(Asignacion).filter(Asignacion.id == asignacion_id).first()
        
        if not asignacion:
            print(f"❌ Asignación {asignacion_id} no existe")
            raise HTTPException(status_code=404, detail=f"Asignación {asignacion_id} no encontrada")
        
        db.delete(asignacion)
        db.commit()
        
        print(f"✅ Asignación {asignacion_id} eliminada")
        
        return {
            "mensaje": "Asignación eliminada",
            "id": asignacion_id
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Error eliminando: {e}")
        raise HTTPException(status_code=500, detail=str(e))