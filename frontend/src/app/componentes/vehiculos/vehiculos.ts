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
  nuevoVehiculo = { 
    marca: '', 
    modelo: '', 
    anio: null as number | null  // ✅ Cambio a number
  };

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.cargarVehiculos();
  }

  cargarVehiculos() {
    this.http.get<any[]>('http://localhost:8000/vehiculos/')  // ✅ Agregué /
      .subscribe({
        next: (data) => {
          console.log('✅ Vehículos cargados:', data);
          this.vehiculos = data;
        },
        error: (err) => {
          console.error('❌ Error al cargar vehículos:', err);
        }
      });
  }

  agregarVehiculo() {
    // ✅ Validación
    if (!this.nuevoVehiculo.marca || !this.nuevoVehiculo.modelo || !this.nuevoVehiculo.anio) {
      alert('Por favor completa todos los campos');
      return;
    }

    // ✅ Asegurar que el año sea número
    const vehiculo = {
      marca: this.nuevoVehiculo.marca.trim(),
      modelo: this.nuevoVehiculo.modelo.trim(),
      anio: Number(this.nuevoVehiculo.anio)
    };

    console.log('📤 Enviando vehículo:', vehiculo);

    this.http.post('http://localhost:8000/vehiculos/', vehiculo)  // ✅ Agregué /
      .subscribe({
        next: (response) => {
          console.log('✅ Vehículo agregado:', response);
          alert('Vehículo agregado correctamente ✅');
          this.cargarVehiculos();
          this.nuevoVehiculo = { marca: '', modelo: '', anio: null };
        },
        error: (err) => {
          console.error('❌ Error completo:', err);
          console.error('❌ Detalles del error:', err.error);
          
          // Mostrar error específico
          let mensaje = 'Error al agregar vehículo';
          if (err.error?.detail) {
            mensaje = err.error.detail;
          } else if (typeof err.error === 'string') {
            mensaje = err.error;
          } else if (err.error) {
            mensaje = JSON.stringify(err.error);
          }
          
          alert(mensaje);
        }
      });
  }
}