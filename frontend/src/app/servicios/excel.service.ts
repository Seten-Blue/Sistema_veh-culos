import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

// Interfaces para tipar las respuestas
export interface ValidacionResponse {
  valido: boolean;
  validaciones: Array<{
    columna: string;
    requerida: boolean;
    valida: boolean;
    mensaje?: string;
  }>; 
  total_columnas: number;
  total_filas: number;
}

export interface PreviewResponse {
  columnas: string[];
  filas: any[];
  total_registros: number;
}

export interface CargaResponse {
  total: number;
  exitosos: number;
  fallidos: number;
  errores: string[];
}

export interface ListarVehiculosResponse {
  total: number;
  vehiculos: Array<{
    id: number;
    marca: string;
    modelo: string;
    anio?: number;
    kilometraje?: number;
    tipo_combustible?: string;
    caballos?: number;
    torque?: number;
    segmento?: string;
  }>;
}

@Injectable({
  providedIn: 'root'
})
export class ExcelService {
  private baseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  // Validar estructura del Excel
  validarArchivo(file: File): Observable<ValidacionResponse> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<ValidacionResponse>(`${this.baseUrl}/excel/validar`, formData);
  }

  // Obtener vista previa
  obtenerPreview(file: File): Observable<PreviewResponse> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<PreviewResponse>(`${this.baseUrl}/excel/preview`, formData);
  }

  // Subir y cargar el archivo Excel (usa /excel/cargar)
  uploadFile(file: File, sessionId: string): Observable<any> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('sessionId', sessionId); // 👈 agrega este campo
  return this.http.post<any>(`${this.baseUrl}/excel/cargar_directo`, formData);
}



  // Listar datos guardados desde la base de datos
  listarVehiculos(): Observable<ListarVehiculosResponse> {
    return this.http.get<ListarVehiculosResponse>(`${this.baseUrl}/excel/listar`);
  }

  // Vaciar tabla (opcional, solo para pruebas)
  limpiarTabla(): Observable<{ mensaje: string }> {
    return this.http.delete<{ mensaje: string }>(`${this.baseUrl}/excel/limpiar`);
  }
}