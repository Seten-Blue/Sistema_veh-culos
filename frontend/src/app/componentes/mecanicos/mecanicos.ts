import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-mecanicos',
  templateUrl: './mecanicos.html',
  styleUrls: ['./mecanicos.scss'],
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule]
})
export class Mecanicos implements OnInit {
  mecanicos: any[] = [];
  nuevoMecanico = { nombre: '', apellido: '' };

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.cargarMecanicos();
  }

  cargarMecanicos() {
    this.http.get<any[]>('http://localhost:8000/mecanicos/')  
      .subscribe(data => this.mecanicos = data);
  }

  agregarMecanico() {
    this.http.post('http://localhost:8000/mecanicos/', this.nuevoMecanico) 
      .subscribe(() => {
        this.cargarMecanicos();
        this.nuevoMecanico = { nombre: '', apellido: '' };
      });
  }
}