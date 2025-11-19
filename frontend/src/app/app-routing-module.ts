import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { Vehiculos } from './componentes/vehiculos/vehiculos';
import { Mecanicos } from './componentes/mecanicos/mecanicos';
import { Asignaciones } from './componentes/asignaciones/asignaciones';

const routes: Routes = [
  { path: '', pathMatch: 'full' },

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
