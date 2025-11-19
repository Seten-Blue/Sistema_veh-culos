import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-asignaciones',
  templateUrl: './asignaciones.html',
  styleUrls: ['./asignaciones.scss'],
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule]
})
export class Asignaciones implements OnInit {
  asignaciones: any[] = [];
  cargando = false;
  error: string = '';
  
  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.cargarAsignaciones();
  }

  cargarAsignaciones() {
    this.cargando = true;
    this.error = '';
    
    this.http.get<any[]>('http://localhost:8000/asignaciones/')
      .subscribe({
        next: (data) => {
          console.log('✅ Asignaciones cargadas:', data);
          this.asignaciones = data;
          this.cargando = false;
        },
        error: (err) => {
          console.error('❌ Error al cargar asignaciones:', err);
          this.error = 'Error al cargar las asignaciones. Por favor, verifica que el servidor esté funcionando.';
          this.cargando = false;
        }
      });
  }

  cambiarEstado(id: number, event: any) {
    const nuevoEstado = event.target.value;
    
    console.log(`Cambiando estado de asignación ${id} a: ${nuevoEstado}`);  // ✅ Paréntesis
    
    this.http.patch(`http://localhost:8000/asignaciones/${id}`, {  // ✅ Paréntesis y sin /
      estado: nuevoEstado 
    })
      .subscribe({
        next: (response) => {
          console.log('✅ Estado actualizado:', response);
          const asignacion = this.asignaciones.find(a => a.id === id);
          if (asignacion) {
            asignacion.estado = nuevoEstado;
          }
        },
        error: (err) => {
          console.error('❌ Error al actualizar estado:', err);
          console.error('Detalles del error:', err.error);
          alert(`Error al actualizar el estado: ${err.error?.detail || 'Error desconocido'}`);  // ✅ Paréntesis
          event.target.value = this.asignaciones.find(a => a.id === id)?.estado || 'Pendiente';
        }
      });
  }

  eliminarAsignacion(id: number) {
    if (!confirm('¿Estás seguro de eliminar esta asignación?')) return;
    
    console.log(`Eliminando asignación ${id}`);  // ✅ Paréntesis
    
    this.http.delete(`http://localhost:8000/asignaciones/${id}`)  // ✅ Paréntesis y sin /
      .subscribe({
        next: (response) => {
          console.log('✅ Asignación eliminada:', response);
          alert('Asignación eliminada correctamente');
          this.asignaciones = this.asignaciones.filter(a => a.id !== id);
        },
        error: (err) => {
          console.error('❌ Error al eliminar:', err);
          console.error('Detalles del error:', err.error);
          alert(`Error al eliminar la asignación: ${err.error?.detail || 'Error desconocido'}`);  // ✅ Paréntesis
        }
      });
  }

  obtenerClaseEstado(estado: string): string {
    switch(estado) {
      case 'Pendiente':
        return 'bg-warning text-dark';
      case 'En Proceso':
        return 'bg-info text-dark';
      case 'Completado':
        return 'bg-success text-white';
      default:
        return 'bg-secondary text-white';
    }
  }
}