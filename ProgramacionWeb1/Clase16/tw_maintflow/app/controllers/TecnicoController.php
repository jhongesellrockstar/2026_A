<?php
class TecnicoController extends CrudController {protected string $table='tecnicos',$pk='id_tecnico',$folder='tecnicos',$label='Técnicos';protected array $fields=['id_usuario'=>'ID usuario','especialidad'=>'Especialidad','telefono'=>'Teléfono','fecha_ingreso'=>'Fecha ingreso','estado'=>'Estado (1/0)'];}

