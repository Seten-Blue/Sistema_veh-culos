import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-vehiculos',
  templateUrl: './vehiculos.html',
  styleUrls: ['./vehiculos.scss'],
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule]
})
export class Vehiculos implements OnInit {
  vehiculos: any[] = [];
  nuevoVehiculo = { marca: '', modelo: '', anio: '' };

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.cargarVehiculos();
  }

  cargarVehiculos() {
    this.http.get<any[]>('http://localhost:8000/vehiculos')
      .subscribe(data => this.vehiculos = data);
  }

  agregarVehiculo() {
    this.http.post('http://localhost:8000/vehiculos', this.nuevoVehiculo)
      .subscribe(() => {
        this.cargarVehiculos();
        this.nuevoVehiculo = { marca: '', modelo: '', anio: '' };
      });
  }
}
