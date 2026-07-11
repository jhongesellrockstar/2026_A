<?php
class ClienteController extends CrudController {protected string $table='clientes',$pk='id_cliente',$folder='clientes',$label='Clientes';protected array $fields=['razon_social'=>'Razón social','ruc'=>'RUC','contacto'=>'Contacto','telefono'=>'Teléfono','correo'=>'Correo','direccion'=>'Dirección','estado'=>'Estado (1/0)'];}

