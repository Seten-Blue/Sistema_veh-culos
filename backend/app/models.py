from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

# ==========================
# MODELOS SQLALCHEMY
# ==========================
class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String(100), nullable=False)
    modelo = Column(String(100), nullable=False)
    kilometraje = Column(String(50), nullable=False)
    tipo_combustible = Column(String(50), nullable=False)
    caballos = Column(String(50), nullable=False)
    torque = Column(String(50), nullable=False)
    segmento = Column(String(50), nullable=False)
    anio = Column(Integer, nullable=True)  # ✅ PUEDE SER NULL


class Mecanico(Base):
    __tablename__ = "mecanicos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)


class Asignacion(Base):
    __tablename__ = "asignaciones"

    id = Column(Integer, primary_key=True, index=True)
    id_vehiculo = Column(Integer, ForeignKey("vehiculos.id"))
    id_mecanico = Column(Integer, ForeignKey("mecanicos.id"))
    descripcion = Column(String(255), default="")
    estado = Column(String(50), default="pendiente")
    fecha_asignacion = Column(DateTime, default=datetime.utcnow)

    vehiculo = relationship("Vehiculo")
    mecanico = relationship("Mecanico")