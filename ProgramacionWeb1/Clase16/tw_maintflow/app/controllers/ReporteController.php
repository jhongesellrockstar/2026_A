<?php
class ReporteController extends Controller {public function index():void{Auth::requireRole(['administrador']);$this->view('reportes/index',['title'=>'Reportes','data'=>(new Reporte())->data()]);}}

