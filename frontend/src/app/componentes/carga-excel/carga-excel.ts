import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { ExcelService } from '../../servicios/excel.service';

interface ColumnValidation {
  columna: string;
  requerida: boolean;
  valida: boolean;
  mensaje?: string;
}

interface PreviewData {
  columnas: string[];
  filas: any[];
  total_registros: number;
}

interface WebSocketMessage {
  tipo: string;
  progreso?: number;
  mensaje?: string;
  total?: number;
  procesados?: number;
  exitosos?: number;
  fallidos?: number;
}

@Component({
  selector: 'app-carga-excel',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule],
  templateUrl: './carga-excel.html',
  styleUrls: ['./carga-excel.scss']
})
export class CargaExcel implements OnInit, OnDestroy {
  archivoSeleccionado: File | null = null;
  nombreArchivo = '';
  validacionColumnas: ColumnValidation[] = [];
  columnasValidas = false;
  previewData: PreviewData | null = null;
  mostrarPreview = false;
  cargando = false;
  progreso = 0;
  mensaje = '';
  resultadoCarga: any = null;
  mostrarResultado = false;
  private ws: WebSocket | null = null;
  private sessionId = '';

  constructor(private excelService: ExcelService) {}

  ngOnInit() {
    this.sessionId = this.generarSessionId();
  }

  ngOnDestroy() {
    this.cerrarWebSocket();
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (!file) return;
    if (!file.name.endsWith('.xlsx') && !file.name.endsWith('.xls')) {
      alert('Solo se permiten archivos Excel (.xlsx o .xls)');
      return;
    }
    this.archivoSeleccionado = file;
    this.nombreArchivo = file.name;
    this.validarArchivo();
  }

  validarArchivo() {
    if (!this.archivoSeleccionado) return;
    this.cargando = true;
    this.mensaje = 'Validando estructura del archivo...';

    this.excelService.validarArchivo(this.archivoSeleccionado).subscribe({
      next: (res) => {
        this.validacionColumnas = res.validaciones;
        this.columnasValidas = res.valido;
        this.mensaje = res.valido ? '✓ Columnas válidas' : '✗ Hay errores';
        this.cargando = false;
        if (res.valido) this.cargarPreview();
      },
      error: () => {
        this.mensaje = 'Error al validar el archivo';
        this.cargando = false;
      }
    });
  }

  cargarPreview() {
    if (!this.archivoSeleccionado) return;
    this.mensaje = 'Cargando vista previa...';
    this.excelService.obtenerPreview(this.archivoSeleccionado).subscribe({
      next: (res) => {
        this.previewData = res;
        this.mostrarPreview = true;
        this.mensaje = `Vista previa lista (${res.total_registros} registros)`;
      },
      error: () => this.mensaje = 'Error al cargar vista previa'
    });
  }

  confirmarCarga() {
    if (!confirm(`¿Deseas cargar ${this.previewData?.total_registros} registros a la base de datos?`)) return;
    this.iniciarCarga();
  }

  iniciarCarga() {
    if (!this.archivoSeleccionado) return;
    this.cargando = true;
    this.progreso = 0;
    this.mensaje = 'Iniciando carga...';
    this.conectarWebSocket();

    this.excelService.uploadFile(this.archivoSeleccionado, this.sessionId).subscribe({
      next: (res) => {
        this.resultadoCarga = res;
        this.mostrarResultado = true;
        this.cargando = false;
      },
      error: () => {
        this.mensaje = 'Error al cargar datos';
        this.cargando = false;
      }
    });
  }

  conectarWebSocket() {
    this.ws = new WebSocket(`ws://localhost:8000/ws/${this.sessionId}`);
    this.ws.onmessage = (event) => {
      const data: WebSocketMessage = JSON.parse(event.data);
      if (data.tipo === 'progreso') {
        this.progreso = data.progreso || 0;
        this.mensaje = data.mensaje || '';
      } else if (data.tipo === 'completado') {
        this.progreso = 100;
        this.mensaje = `Completado (${data.exitosos} exitosos, ${data.fallidos} fallidos)`;
      }
    };
  }

  cerrarWebSocket() {
    this.ws?.close();
  }

  generarSessionId(): string {
    return 'session_' + Math.random().toString(36).substring(2, 10);
  }

  resetearFormulario() {
    this.archivoSeleccionado = null;
    this.nombreArchivo = '';
    this.validacionColumnas = [];
    this.previewData = null;
    this.mostrarPreview = false;
    this.resultadoCarga = null;
    this.mostrarResultado = false;
    this.mensaje = '';
    this.progreso = 0;
  }
}
