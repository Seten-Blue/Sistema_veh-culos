import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MecanicosService {
  private apiUrl = 'http://localhost:8000/mecanicos/';

  constructor(private http: HttpClient) {}

  obtenerMecanicos(): Observable<any> {
    return this.http.get(this.apiUrl);
  }

  agregarMecanico(mecanico: any): Observable<any> {
    return this.http.post(this.apiUrl, mecanico);
  }

  actualizarMecanico(id: number, mecanico: any): Observable<any> {
    return this.http.put(`${this.apiUrl}${id}/`, mecanico);  // ✅ Paréntesis agregados
  }

  eliminarMecanico(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}${id}/`);  // ✅ Paréntesis agregados
  }
}