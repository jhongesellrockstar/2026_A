<?php
class SedeController extends CrudController {protected string $table='sedes',$pk='id_sede',$folder='sedes',$label='Sedes';protected array $fields=['id_cliente'=>'ID cliente','nombre_sede'=>'Nombre','direccion'=>'Dirección','distrito'=>'Distrito','provincia'=>'Provincia','departamento'=>'Departamento','estado'=>'Estado (1/0)'];}

