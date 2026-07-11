<?php
class UsuarioController extends Controller {public function index():void{Auth::requireRole(['administrador']);$this->view('usuarios/index',['title'=>'Usuarios','rows'=>(new Usuario())->all()]);}}

