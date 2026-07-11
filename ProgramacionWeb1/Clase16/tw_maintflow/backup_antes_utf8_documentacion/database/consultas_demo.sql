USE bd_tw_maintflow;
SELECT o.id_orden,e.nombre_equipo,es.nombre_estado FROM ordenes_servicio o JOIN equipos e ON e.id_equipo=o.id_equipo JOIN estados_orden es ON es.id_estado=o.id_estado;
SELECT es.nombre_estado,COUNT(*) total FROM ordenes_servicio o JOIN estados_orden es ON es.id_estado=o.id_estado GROUP BY es.id_estado;
SELECT CONCAT(u.nombres,' ',u.apellidos) tecnico,COUNT(o.id_orden) total FROM tecnicos t JOIN usuarios u ON u.id_usuario=t.id_usuario LEFT JOIN ordenes_servicio o ON o.id_tecnico=t.id_tecnico GROUP BY t.id_tecnico;
SELECT c.razon_social,COUNT(o.id_orden) total FROM clientes c JOIN sedes s ON s.id_cliente=c.id_cliente JOIN equipos e ON e.id_sede=s.id_sede LEFT JOIN ordenes_servicio o ON o.id_equipo=e.id_equipo GROUP BY c.id_cliente;
SELECT s.nombre_sede,COUNT(e.id_equipo) equipos FROM sedes s LEFT JOIN equipos e ON e.id_sede=s.id_sede GROUP BY s.id_sede;
SELECT * FROM repuestos WHERE stock_actual<=stock_minimo;
SELECT r.nombre_repuesto,SUM(m.cantidad) consumo FROM movimientos_repuesto m JOIN repuestos r ON r.id_repuesto=m.id_repuesto WHERE m.tipo_movimiento='Salida' GROUP BY r.id_repuesto;
SELECT id_orden,costo_mano_obra,costo_total FROM ordenes_servicio ORDER BY costo_total DESC;
SELECT * FROM ordenes_servicio WHERE fecha_solicitud BETWEEN '2026-06-01' AND '2026-07-31';
SELECT tipo_mantenimiento,AVG(costo_total) promedio FROM ordenes_servicio GROUP BY tipo_mantenimiento;
SELECT prioridad,COUNT(*) total FROM ordenes_servicio GROUP BY prioridad HAVING COUNT(*)>=1;
SELECT c.nombre_categoria,COUNT(e.id_equipo) total FROM categorias_equipo c LEFT JOIN equipos e ON e.id_categoria=c.id_categoria GROUP BY c.id_categoria;
SELECT SUM(costo_total) costo_global FROM ordenes_servicio;
SELECT r.nombre_repuesto,SUM(d.cantidad) usado FROM detalle_orden d JOIN repuestos r ON r.id_repuesto=d.id_repuesto GROUP BY r.id_repuesto;
SELECT c.razon_social,s.nombre_sede,e.codigo_equipo,e.nombre_equipo FROM clientes c JOIN sedes s ON s.id_cliente=c.id_cliente JOIN equipos e ON e.id_sede=s.id_sede ORDER BY c.razon_social;

