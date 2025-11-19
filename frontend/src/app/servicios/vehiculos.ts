import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class VehiculosService {  // <-- Asegúrate de que tenga 'export'
  private apiUrl = 'http://localhost:8000/vehiculos';

  constructor(private http: HttpClient) {}

  obtenerVehiculos(): Observable<any> {
    return this.http.get(this.apiUrl);
  }

  crearVehiculo(vehiculo: any): Observable<any> {
    return this.http.post(this.apiUrl, vehiculo);
  }

  actualizarVehiculo(id: number, vehiculo: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}`, vehiculo);
  }

  eliminarVehiculo(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }
}