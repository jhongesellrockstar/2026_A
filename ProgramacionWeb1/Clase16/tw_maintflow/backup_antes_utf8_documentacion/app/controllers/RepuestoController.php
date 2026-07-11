<?php
class RepuestoController extends CrudController {protected string $table='repuestos',$pk='id_repuesto',$folder='repuestos',$label='Repuestos';protected array $fields=['codigo_repuesto'=>'Código','nombre_repuesto'=>'Nombre','descripcion'=>'Descripción','unidad_medida'=>'Unidad','stock_actual'=>'Stock','stock_minimo'=>'Stock mínimo','precio_unitario'=>'Precio','estado'=>'Estado (1/0)'];}

