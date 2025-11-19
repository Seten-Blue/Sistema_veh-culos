from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ========================
# VEHICULOS
# ========================
class VehiculoCreate(BaseModel):
    marca: str
    modelo: str
    anio: Optional[int] = None  # ✅ OPCIONAL - puede ser None
    kilometraje: str
    tipo_combustible: str
    caballos: str
    torque: str
    segmento: str

class VehiculoResponse(BaseModel):
    id: int
    marca: str
    modelo: str
    anio: Optional[int] = None  # ✅ OPCIONAL - puede ser None
    kilometraje: str
    tipo_combustible: str
    caballos: str
    torque: str
    segmento: str

    class Config:
        from_attributes = True  # ✅ CAMBIO: Pydantic V2 usa 'from_attributes' en vez de 'orm_mode'

class VehiculoUpdate(BaseModel):
    marca: Optional[str] = None
    modelo: Optional[str] = None
    anio: Optional[int] = None
    kilometraje: Optional[str] = None
    tipo_combustible: Optional[str] = None
    caballos: Optional[str] = None
    torque: Optional[str] = None
    segmento: Optional[str] = None

# ========================
# MECANICOS
# ========================
class MecanicoCreate(BaseModel):
    nombre: str
    apellido: str

class MecanicoResponse(BaseModel):
    id: int
    nombre: str
    apellido: str

    class Config:
        from_attributes = True  # ✅ CAMBIO: Pydantic V2

# ========================
# ASIGNACIONES
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
        from_attributes = True  # ✅ CAMBIO: Pydantic V2