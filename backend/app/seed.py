from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Vehiculo, Mecanico

# Abrir sesión
db: Session = SessionLocal()

# Lista de 10 vehículos de ejemplo
vehiculos = [
    {"marca": "Tesla", "modelo": "Model S", "kilometraje": "0 km", "tipo_combustible": "Eléctrico", "caballos": "670", "torque": "1050 Nm", "segmento": "Premium"},
    {"marca": "Nissan", "modelo": "Leaf", "kilometraje": "0 km", "tipo_combustible": "Eléctrico", "caballos": "147", "torque": "320 Nm", "segmento": "Compacto"},
    {"marca": "Chevrolet", "modelo": "Bolt", "kilometraje": "0 km", "tipo_combustible": "Eléctrico", "caballos": "200", "torque": "360 Nm", "segmento": "Compacto"},
    {"marca": "BMW", "modelo": "i3", "kilometraje": "0 km", "tipo_combustible": "Eléctrico", "caballos": "170", "torque": "250 Nm", "segmento": "Subcompacto"},
    {"marca": "Audi", "modelo": "e-tron", "kilometraje": "0 km", "tipo_combustible": "Eléctrico", "caballos": "355", "torque": "561 Nm", "segmento": "SUV"},
    {"marca": "Ford", "modelo": "Mustang Mach-E", "kilometraje": "0 km", "tipo_combustible": "Eléctrico", "caballos": "346", "torque": "580 Nm", "segmento": "SUV"},
    {"marca": "Hyundai", "modelo": "Kona Electric", "kilometraje": "0 km", "tipo_combustible": "Eléctrico", "caballos": "201", "torque": "395 Nm", "segmento": "SUV"},
    {"marca": "Kia", "modelo": "Soul EV", "kilometraje": "0 km", "tipo_combustible": "Eléctrico", "caballos": "201", "torque": "395 Nm", "segmento": "Subcompacto"},
    {"marca": "Porsche", "modelo": "Taycan", "kilometraje": "0 km", "tipo_combustible": "Eléctrico", "caballos": "522", "torque": "650 Nm", "segmento": "Premium"},
    {"marca": "Volkswagen", "modelo": "ID.4", "kilometraje": "0 km", "tipo_combustible": "Eléctrico", "caballos": "201", "torque": "310 Nm", "segmento": "SUV"},
]

# Lista de 10 mecánicos de ejemplo
mecanicos = [
    {"nombre": "Juan", "apellido": "Pérez"},
    {"nombre": "Ana", "apellido": "Gómez"},
    {"nombre": "Luis", "apellido": "Martínez"},
    {"nombre": "María", "apellido": "Rodríguez"},
    {"nombre": "Carlos", "apellido": "López"},
    {"nombre": "Sofía", "apellido": "Hernández"},
    {"nombre": "Andrés", "apellido": "García"},
    {"nombre": "Paula", "apellido": "Jiménez"},
    {"nombre": "Diego", "apellido": "Santos"},
    {"nombre": "Camila", "apellido": "Torres"},
]

# Agregar vehículos
for v in vehiculos:
    vehiculo = Vehiculo(**v)
    db.add(vehiculo)

# Agregar mecánicos
for m in mecanicos:
    mecanico = Mecanico(**m)
    db.add(mecanico)

# Guardar cambios
db.commit()
db.close()

print("Se agregaron 10 vehículos y 10 mecánicos con éxito!")
