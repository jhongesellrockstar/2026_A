USE northwind;

DROP FUNCTION IF EXISTS fn_TotalProductosCategoria;
DROP FUNCTION IF EXISTS fn_DescuentoProducto;

DELIMITER $$

-- Pregunta 7
-- Retorna la cantidad total de productos de una categoria.
CREATE FUNCTION fn_TotalProductosCategoria(p_category_id INT)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_total INT;

    SELECT COUNT(*)
    INTO v_total
    FROM products
    WHERE CategoryID = p_category_id;

    RETURN v_total;
END$$

-- Pregunta 8
-- Indica si un producto aplica descuento segun su precio.
CREATE FUNCTION fn_DescuentoProducto(p_product_id INT)
RETURNS VARCHAR(20)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_precio DECIMAL(10, 2);

    SELECT UnitPrice
    INTO v_precio
    FROM products
    WHERE ProductID = p_product_id
    LIMIT 1;

    IF v_precio > 50 THEN
        RETURN 'APLICA DESCUENTO';
    ELSE
        RETURN 'SIN DESCUENTO';
    END IF;
END$$

DELIMITER ;

-- Ejemplos:
-- SELECT fn_TotalProductosCategoria(1);
-- SELECT fn_DescuentoProducto(5);
