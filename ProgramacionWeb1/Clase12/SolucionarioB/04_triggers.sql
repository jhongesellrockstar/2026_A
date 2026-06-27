USE northwind;

DROP TRIGGER IF EXISTS trg_clientes_validar_companyname;
DROP TRIGGER IF EXISTS trg_productos_eliminados;

CREATE TABLE IF NOT EXISTS productos_eliminados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    fecha_eliminacion DATETIME NOT NULL
);

DELIMITER $$

-- Pregunta 9
-- Valida que CompanyName no este vacio antes de insertar un cliente.
CREATE TRIGGER trg_clientes_validar_companyname
BEFORE INSERT ON customers
FOR EACH ROW
BEGIN
    IF NEW.CompanyName IS NULL OR TRIM(NEW.CompanyName) = '' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'El nombre de la empresa es obligatorio';
    END IF;
END$$

-- Pregunta 10
-- Registra la informacion del producto eliminado.
CREATE TRIGGER trg_productos_eliminados
AFTER DELETE ON products
FOR EACH ROW
BEGIN
    INSERT INTO productos_eliminados (
        product_id,
        product_name,
        fecha_eliminacion
    )
    VALUES (
        OLD.ProductID,
        OLD.ProductName,
        NOW()
    );
END$$

DELIMITER ;
