<?php
class EquipoController extends CrudController {protected string $table='equipos',$pk='id_equipo',$folder='equipos',$label='Equipos';protected array $fields=['id_sede'=>'ID sede','id_categoria'=>'ID categoría','codigo_equipo'=>'Código','nombre_equipo'=>'Nombre','marca'=>'Marca','modelo'=>'Modelo','numero_serie'=>'Serie','fecha_adquisicion'=>'Fecha adquisición','estado_operativo'=>'Estado operativo','observaciones'=>'Observaciones'];}

