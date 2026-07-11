<?php
class Usuario extends Model {
    public function authenticate(string $username,string $password):?array{$q=$this->db->prepare('SELECT u.*,r.nombre_rol rol FROM usuarios u JOIN roles r ON r.id_rol=u.id_rol WHERE u.username=? AND u.estado=1');$q->execute([$username]);$u=$q->fetch();return $u&&password_verify($password,$u['password_hash'])?$u:null;}
    public function all():array{return $this->db->query('SELECT u.id_usuario,u.username,u.nombres,u.apellidos,u.correo,u.estado,r.nombre_rol FROM usuarios u JOIN roles r ON r.id_rol=u.id_rol ORDER BY u.id_usuario')->fetchAll();}
}

