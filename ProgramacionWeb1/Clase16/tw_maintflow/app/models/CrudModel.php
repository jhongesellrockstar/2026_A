<?php
class CrudModel extends Model {
    private const ALLOWED = [
        'clientes'=>['razon_social','ruc','contacto','telefono','correo','direccion','estado'],
        'sedes'=>['id_cliente','nombre_sede','direccion','distrito','provincia','departamento','estado'],
        'equipos'=>['id_sede','id_categoria','codigo_equipo','nombre_equipo','marca','modelo','numero_serie','fecha_adquisicion','estado_operativo','observaciones'],
        'tecnicos'=>['id_usuario','especialidad','telefono','fecha_ingreso','estado'],
        'repuestos'=>['codigo_repuesto','nombre_repuesto','descripcion','unidad_medida','stock_actual','stock_minimo','precio_unitario','estado'],
    ];
    public function all(string $table): array { $this->guard($table); return $this->db->query("SELECT * FROM `$table` ORDER BY 1 DESC")->fetchAll(); }
    public function find(string $table, string $pk, int $id): ?array { $this->guard($table); $q=$this->db->prepare("SELECT * FROM `$table` WHERE `$pk`=?"); $q->execute([$id]); return $q->fetch() ?: null; }
    public function save(string $table, string $pk, array $input, int $id=0): void {
        $this->guard($table); $data=[]; foreach(self::ALLOWED[$table] as $f) if(array_key_exists($f,$input)) $data[$f]=trim((string)$input[$f]);
        if (!$data) throw new InvalidArgumentException('No hay datos válidos.');
        if($id){$set=implode(',',array_map(fn($f)=>"`$f`=?",array_keys($data)));$q=$this->db->prepare("UPDATE `$table` SET $set WHERE `$pk`=?");$q->execute([...array_values($data),$id]);}
        else {$fields='`'.implode('`,`',array_keys($data)).'`';$marks=implode(',',array_fill(0,count($data),'?'));$q=$this->db->prepare("INSERT INTO `$table` ($fields) VALUES ($marks)");$q->execute(array_values($data));}
    }
    public function deactivate(string $table,string $pk,int $id):void{$this->guard($table);$q=$this->db->prepare("UPDATE `$table` SET estado=0 WHERE `$pk`=?");$q->execute([$id]);}
    private function guard(string $table):void{if(!isset(self::ALLOWED[$table]))throw new InvalidArgumentException('Tabla no permitida');}
}

