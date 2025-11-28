import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AsignacionesService {
  private apiUrl = 'http://localhost:8000/asignaciones/';

  constructor(private http: HttpClient) {}

  obtenerAsignaciones(): Observable<any> {
    return this.http.get(this.apiUrl);
  }

  agregarAsignacion(asignacion: any): Observable<any> {
    return this.http.post(this.apiUrl, asignacion);
  }

  actualizarAsignacion(id: number, asignacion: any): Observable<any> {
    return this.http.put(`${this.apiUrl}${id}`, asignacion);  // ✅ Sin / al final
  }

  eliminarAsignacion(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}${id}`);  // ✅ Sin / al final
  }
}