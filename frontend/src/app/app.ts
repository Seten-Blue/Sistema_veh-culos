import { Component, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { Vehiculos } from './componentes/vehiculos/vehiculos';
import { Mecanicos } from './componentes/mecanicos/mecanicos';
import { Asignaciones } from './componentes/asignaciones/asignaciones';
import { bootstrapApplication } from '@angular/platform-browser';
import { CargaExcel } from './componentes/carga-excel/carga-excel';
import { VehiculosService } from './servicios/vehiculos';
import { MecanicosService } from './servicios/mecanicos';
import { AsignacionesService } from './servicios/asignaciones';
import { ExcelService } from './servicios/excel.service';
import * as XLSX from 'xlsx';

declare var bootstrap: any;

// ==========================
// INTERFACES
// ==========================
interface Vehiculo {
  marca: string;
  modelo: string;
  anio: string;
  kilometraje: string;
  tipo_combustible: string;
  caballos: string;
  torque: string;
  segmento: string;
}

interface Mecanico {
  nombre: string;
  apellido: string;
}

interface Asignacion {
  id_mecanico: number;  // ✅ Cambiado a number
  id_vehiculo: number;  // ✅ Cambiado a number
  descripcion: string;
  estado: string;
}

// ==========================
// COMPONENTE PRINCIPAL
// ==========================
@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  styleUrls: ['./app.scss'],
  standalone: true,
  imports: [
    CommonModule, 
    FormsModule, 
    HttpClientModule, 
    Vehiculos, 
    Mecanicos, 
    Asignaciones,
    CargaExcel
  ]
})
export class AppComponent implements AfterViewInit {
  titulo = 'Dashboard Vehículos y Mecánicos';
  mostrarCargaExcel = false;

  // ==========================
  // NUEVAS VARIABLES PARA EL EXCEL
  // ==========================
  archivoSeleccionado: File | null = null;
  mensaje: string = '';
  private sessionId = '';

  // ==========================
  // OBJETOS
  // ==========================
  nuevoVehiculo: Vehiculo = {
    marca: '', modelo: '', anio: '', kilometraje: '',
    tipo_combustible: '', caballos: '', torque: '', segmento: ''
  };

  nuevoMecanico: Mecanico = {
    nombre: '', apellido: ''
  };

  nuevaAsignacion: Asignacion = {
    id_mecanico: 0,  // ✅ Cambiado a 0
    id_vehiculo: 0,  // ✅ Cambiado a 0
    descripcion: '', 
    estado: 'pendiente'
  };

  // ==========================
  // MODALES
  // ==========================
  @ViewChild('modalVehiculo') modalVehiculo!: ElementRef;
  @ViewChild('modalMecanico') modalMecanico!: ElementRef;
  @ViewChild('modalAsignacion') modalAsignacion!: ElementRef;

  private bootstrapModalVehiculo: any;
  private bootstrapModalMecanico: any;
  private bootstrapModalAsignacion: any;

  constructor(
    private vehiculosService: VehiculosService,
    private mecanicosService: MecanicosService,
    private asignacionesService: AsignacionesService,
    private excelService: ExcelService
  ) {
    this.sessionId = this.generarSessionId();
  }

  ngAfterViewInit(): void {
    this.bootstrapModalVehiculo = new bootstrap.Modal(this.modalVehiculo.nativeElement, { backdrop: 'static', keyboard: true });
    this.bootstrapModalMecanico = new bootstrap.Modal(this.modalMecanico.nativeElement, { backdrop: 'static', keyboard: true });
    this.bootstrapModalAsignacion = new bootstrap.Modal(this.modalAsignacion.nativeElement, { backdrop: 'static', keyboard: true });
  }

  // ==========================
  // TOGGLE EXCEL
  // ==========================
  toggleCargaExcel() {
    this.mostrarCargaExcel = !this.mostrarCargaExcel;
  }

  // ==========================
  // FUNCIONES DE EXCEL
  // ==========================
  onFileSelected(event: any) {
    this.archivoSeleccionado = event.target.files[0];
    console.log('Archivo seleccionado:', this.archivoSeleccionado);
  }

  cargarArchivo() {
    if (!this.archivoSeleccionado) {
      this.mensaje = 'Por favor selecciona un archivo primero ❗';
      return;
    }

    this.mensaje = '📤 Subiendo archivo al servidor...';

    this.excelService.uploadFile(this.archivoSeleccionado, this.sessionId).subscribe({
      next: (response) => {
        console.log('✅ Respuesta del backend:', response);
        this.mensaje = `✅ ${response.exitosos} registros guardados correctamente en la base de datos`;
        
        if (response.fallidos > 0) {
          this.mensaje += ` (${response.fallidos} fallidos)`;
          console.error('Errores:', response.errores);
        }
        
        setTimeout(() => {
          window.location.reload();
        }, 2000);
      },
      error: (err) => {
        console.error('❌ Error al subir archivo:', err);
        this.mensaje = '❌ Error al cargar el archivo al servidor';
      }
    });
  }

  generarSessionId(): string {
    return 'session_' + Math.random().toString(36).substring(2, 10);
  }

  // ==========================
  // FUNCIONES DE MODALES
  // ==========================
  abrirModal(modal: string) {
    if (modal === 'vehiculo') this.bootstrapModalVehiculo.show();
    if (modal === 'mecanico') this.bootstrapModalMecanico.show();
    if (modal === 'asignacion') this.bootstrapModalAsignacion.show();
  }

  cerrarModal(modal: string) {
    if (modal === 'vehiculo') this.bootstrapModalVehiculo.hide();
    if (modal === 'mecanico') this.bootstrapModalMecanico.hide();
    if (modal === 'asignacion') this.bootstrapModalAsignacion.hide();
  }

  // ==========================
  // FUNCIONES AGREGAR
  // ==========================
  agregarVehiculo() {
    if (!this.nuevoVehiculo.marca || !this.nuevoVehiculo.modelo || !this.nuevoVehiculo.anio ||
        !this.nuevoVehiculo.kilometraje || !this.nuevoVehiculo.tipo_combustible ||
        !this.nuevoVehiculo.caballos || !this.nuevoVehiculo.torque || !this.nuevoVehiculo.segmento) {
      alert('Completa todos los campos del vehículo');
      return;
    }
    this.vehiculosService.crearVehiculo(this.nuevoVehiculo).subscribe(() => {
      alert('Vehículo agregado exitosamente');
      this.nuevoVehiculo = { marca: '', modelo: '', anio: '', kilometraje: '', tipo_combustible: '', caballos: '', torque: '', segmento: '' };
      this.cerrarModal('vehiculo');
      window.location.reload();
    });
  }

  agregarMecanico() {
    if (!this.nuevoMecanico.nombre || !this.nuevoMecanico.apellido) {
      alert('Completa todos los campos del mecánico');
      return;
    }
    this.mecanicosService.agregarMecanico(this.nuevoMecanico).subscribe(() => {
      alert('Mecánico agregado exitosamente');
      this.nuevoMecanico = { nombre: '', apellido: '' };
      this.cerrarModal('mecanico');
      window.location.reload();
    });
  }

  agregarAsignacion() {
    if (!this.nuevaAsignacion.id_mecanico || !this.nuevaAsignacion.id_vehiculo ||
        !this.nuevaAsignacion.descripcion || !this.nuevaAsignacion.estado) {
      alert('Completa todos los campos de asignación');
      return;
    }
    this.asignacionesService.agregarAsignacion(this.nuevaAsignacion).subscribe(() => {
      alert('Asignación agregada exitosamente');
      this.nuevaAsignacion = { id_mecanico: 0, id_vehiculo: 0, descripcion: '', estado: 'pendiente' };  // ✅ Cambiado a 0
      this.cerrarModal('asignacion');
      window.location.reload();
    });
  }
}