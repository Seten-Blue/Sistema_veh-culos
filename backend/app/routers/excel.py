from fastapi import APIRouter, UploadFile, File, WebSocket, WebSocketDisconnect, Depends, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import pandas as pd
import io
import json
from typing import List, Dict, Any
from datetime import datetime
from app.database import SessionLocal
from app.models import Vehiculo  # Ajusta según tu modelo
import asyncio

router = APIRouter(
    prefix="/excel",
    tags=["Excel"]
)

# ==========================================
# DEPENDENCIA DE BASE DE DATOS
# ==========================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# GESTIÓN DE WEBSOCKETS
# ==========================================
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
        print(f"WebSocket conectado: {session_id}")

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
            print(f"WebSocket desconectado: {session_id}")

    async def send_message(self, session_id: str, message: dict):
        if session_id in self.active_connections:
            try:
                await self.active_connections[session_id].send_text(json.dumps(message))
            except Exception as e:
                print(f"Error enviando mensaje: {e}")

manager = ConnectionManager()

# ==========================================
# WEBSOCKET ENDPOINT
# ==========================================
@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(websocket, session_id)
    try:
        while True:
            data = await websocket.receive_text()  # Mantener conexión activa
    except WebSocketDisconnect:
        manager.disconnect(session_id)

# ==========================================
# CONFIGURACIÓN DE COLUMNAS ESPERADAS
# ==========================================
COLUMNAS_REQUERIDAS = {
    'marca': {'requerida': True, 'tipo': str},
    'modelo': {'requerida': True, 'tipo': str},
    'anio': {'requerida': True, 'tipo': int},
    'kilometraje': {'requerida': True, 'tipo': int},
    'tipo_combustible': {'requerida': True, 'tipo': str},
    'caballos': {'requerida': True, 'tipo': int},
    'torque': {'requerida': True, 'tipo': int},
    'segmento': {'requerida': True, 'tipo': str}
}

# ==========================================
# ENDPOINT 1: VALIDAR COLUMNAS
# ==========================================
@router.post("/validar")
async def validar_excel(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
        columnas_archivo = set(df.columns)
        validaciones = []
        todas_validas = True

        for col, config in COLUMNAS_REQUERIDAS.items():
            if config['requerida']:
                if col in columnas_archivo:
                    validaciones.append({
                        'columna': col,
                        'requerida': True,
                        'valida': True,
                        'mensaje': 'Columna encontrada ✓'
                    })
                else:
                    validaciones.append({
                        'columna': col,
                        'requerida': True,
                        'valida': False,
                        'mensaje': 'Columna faltante ✗'
                    })
                    todas_validas = False

        columnas_extra = columnas_archivo - set(COLUMNAS_REQUERIDAS.keys())
        for col in columnas_extra:
            validaciones.append({
                'columna': col,
                'requerida': False,
                'valida': True,
                'mensaje': 'Columna adicional (se ignorará)'
            })
        
        return {
            'valido': todas_validas,
            'validaciones': validaciones,
            'total_columnas': len(df.columns),
            'total_filas': len(df)
        }
    except Exception as e:
        return JSONResponse(status_code=400, content={'error': f'Error al leer archivo: {str(e)}'})

# ==========================================
# ENDPOINT 2: PREVIEW DE DATOS
# ==========================================
@router.post("/preview")
async def preview_excel(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
        preview_df = df.head(10)
        preview_data = preview_df.to_dict('records')
        return {
            'columnas': list(df.columns),
            'filas': preview_data,
            'total_registros': len(df)
        }
    except Exception as e:
        return JSONResponse(status_code=400, content={'error': f'Error al generar preview: {str(e)}'})

# ==========================================
# ENDPOINT 3: CARGAR DATOS CON WEBSOCKET
# ==========================================
@router.post("/cargar")
async def cargar_excel(
    file: UploadFile = File(...),
    session_id: str = Form(...),
    db: Session = Depends(get_db)
):
    exitosos = 0
    fallidos = 0
    errores = []
    
    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
        total_registros = len(df)
        
        await manager.send_message(session_id, {
            'tipo': 'progreso',
            'progreso': 0,
            'mensaje': f'Iniciando carga de {total_registros} registros...'
        })
        
        for idx, row in df.iterrows():
            try:
                if pd.isna(row.get('marca')) or pd.isna(row.get('modelo')):
                    raise ValueError("Marca o modelo faltante")
                
                vehiculo = Vehiculo(
                    marca=str(row['marca']).strip(),
                    modelo=str(row['modelo']).strip(),
                    anio=int(row['anio']) if pd.notna(row.get('anio')) else None,
                    kilometraje=int(row['kilometraje']) if pd.notna(row.get('kilometraje')) else None,
                    tipo_combustible=str(row['tipo_combustible']).strip() if pd.notna(row.get('tipo_combustible')) else None,
                    caballos=int(row['caballos']) if pd.notna(row.get('caballos')) else None,
                    torque=int(row['torque']) if pd.notna(row.get('torque')) else None,
                    segmento=str(row['segmento']).strip() if pd.notna(row.get('segmento')) else None
                )
                
                db.add(vehiculo)
                exitosos += 1
                
                if (idx + 1) % 10 == 0:
                    progreso = int(((idx + 1) / total_registros) * 100)
                    await manager.send_message(session_id, {
                        'tipo': 'progreso',
                        'progreso': progreso,
                        'mensaje': f'Procesando... {idx + 1}/{total_registros}',
                        'exitosos': exitosos,
                        'fallidos': fallidos
                    })
                    db.commit()
                
            except Exception as e:
                fallidos += 1
                error_msg = f"Fila {idx + 1}: {str(e)}"
                errores.append(error_msg)
                print(error_msg)
                db.rollback()
        
        db.commit()
        
        await manager.send_message(session_id, {
            'tipo': 'completado',
            'progreso': 100,
            'mensaje': 'Carga completada',
            'total': total_registros,
            'exitosos': exitosos,
            'fallidos': fallidos
        })
        
        return {
            'total': total_registros,
            'exitosos': exitosos,
            'fallidos': fallidos,
            'errores': errores[:50]
        }
    except Exception as e:
        db.rollback()
        await manager.send_message(session_id, {'tipo': 'error', 'mensaje': str(e)})
        return JSONResponse(status_code=500, content={'error': f'Error en carga: {str(e)}'})

# ==========================================
# ✅ ENDPOINT 3B: CARGA DIRECTA SIN WEBSOCKET
# ==========================================
@router.post("/cargar_directo")
async def cargar_excel_directo(
    file: UploadFile = File(...),
    sessionId: str = Form(None),  # ← Hacerlo opcional
    db: Session = Depends(get_db)
):
    exitosos = 0
    errores = []

    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')

        columnas_requeridas = {"marca", "modelo", "anio", "kilometraje", "tipo_combustible", "caballos", "torque", "segmento"}
        if not columnas_requeridas.issubset(df.columns):
            faltantes = columnas_requeridas - set(df.columns)
            return JSONResponse(status_code=400, content={"error": f"Columnas faltantes: {', '.join(faltantes)}"})

        for _, row in df.iterrows():
            try:
                vehiculo = Vehiculo(
                    marca=str(row["marca"]).strip(),
                    modelo=str(row["modelo"]).strip(),
                    anio=int(row["anio"]) if pd.notna(row["anio"]) else None,
                    kilometraje=int(row["kilometraje"]) if pd.notna(row["kilometraje"]) else None,
                    tipo_combustible=str(row["tipo_combustible"]).strip() if pd.notna(row["tipo_combustible"]) else None,
                    caballos=int(row["caballos"]) if pd.notna(row["caballos"]) else None,
                    torque=int(row["torque"]) if pd.notna(row["torque"]) else None,
                    segmento=str(row["segmento"]).strip() if pd.notna(row["segmento"]) else None
                )
                db.add(vehiculo)
                exitosos += 1
            except Exception as e:
                errores.append(str(e))
                
        db.commit()

        return {"mensaje": f"✅ {exitosos} registros guardados correctamente.", "exitosos": exitosos, "fallidos": len(errores), "errores": errores[:10]}
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"error": f"Error al procesar el Excel: {str(e)}"})
# ==========================================
# ENDPOINT 4: LISTAR DATOS CARGADOS
# ==========================================
@router.get("/listar")
async def listar_vehiculos(db: Session = Depends(get_db)):
    """
    Devuelve todos los vehículos cargados desde la base de datos.
    """
    try:
        vehiculos = db.query(Vehiculo).all()
        data = [
            {
                "id": v.id,
                "marca": v.marca,
                "modelo": v.modelo,
                "anio": v.anio,
                "kilometraje": v.kilometraje,
                "tipo_combustible": v.tipo_combustible,
                "caballos": v.caballos,
                "torque": v.torque,
                "segmento": v.segmento
            }
            for v in vehiculos
        ]
        return {"total": len(data), "vehiculos": data}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ==========================================
# ENDPOINT 5: LIMPIAR TABLA VEHICULOS
# ==========================================
@router.delete("/limpiar")
async def limpiar_tabla(db: Session = Depends(get_db)):
    """
    Elimina todos los registros de la tabla vehículos (solo para pruebas).
    """
    try:
        db.query(Vehiculo).delete()
        db.commit()
        return {"mensaje": "Tabla de vehículos vaciada correctamente"}
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"error": str(e)})
