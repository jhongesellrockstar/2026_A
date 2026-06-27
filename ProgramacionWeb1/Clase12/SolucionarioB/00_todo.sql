USE northwind;

-- ============================================================
-- PARTE I: CONSULTAS SQL
-- ============================================================

-- Pregunta 1
SELECT
    ProductID,
    ProductName,
    UnitsInStock
FROM products
WHERE UnitsInStock > (
    SELECT AVG(UnitsInStock)
    FROM products
)
ORDER BY UnitsInStock DESC;

-- Pregunta 2
SELECT
    s.SupplierID,
    s.CompanyName,
    COUNT(p.ProductID) AS TotalProductos
FROM suppliers AS s
INNER JOIN products AS p
    ON p.SupplierID = s.SupplierID
GROUP BY
    s.SupplierID,
    s.CompanyName
ORDER BY TotalProductos DESC
LIMIT 5;

-- Pregunta 3
SELECT
    e.EmployeeID,
    CONCAT(e.FirstName, ' ', e.LastName) AS NombreCompleto,
    ROUND(SUM(od.Quantity * od.UnitPrice * (1 - od.Discount)), 2) AS TotalVentas
FROM employees AS e
INNER JOIN orders AS o
    ON o.EmployeeID = e.EmployeeID
INNER JOIN order_details AS od
    ON od.OrderID = o.OrderID
GROUP BY
    e.EmployeeID,
    e.FirstName,
    e.LastName
ORDER BY TotalVentas DESC;

-- Pregunta 4
SELECT
    c.CategoryID,
    c.CategoryName,
    COUNT(p.ProductID) AS CantidadProductos
FROM categories AS c
INNER JOIN products AS p
    ON p.CategoryID = c.CategoryID
GROUP BY
    c.CategoryID,
    c.CategoryName
HAVING COUNT(p.ProductID) > 10
ORDER BY CantidadProductos DESC;

-- ============================================================
-- PARTE II: PROCEDIMIENTOS ALMACENADOS
-- ============================================================

DROP PROCEDURE IF EXISTS sp_ProductosProveedor;
DROP PROCEDURE IF EXISTS sp_PedidosCliente;
DROP PROCEDURE IF EXISTS sp_Top5ClientesCompradores;

DELIMITER $$

CREATE PROCEDURE sp_ProductosProveedor(IN p_nombre_proveedor VARCHAR(100))
BEGIN
    SELECT
        p.ProductID,
        p.ProductName,
        p.SupplierID,
        s.CompanyName,
        p.UnitPrice,
        p.UnitsInStock
    FROM products AS p
    INNER JOIN suppliers AS s
        ON s.SupplierID = p.SupplierID
    WHERE s.CompanyName = p_nombre_proveedor
    ORDER BY p.ProductName;
END$$

CREATE PROCEDURE sp_PedidosCliente(IN p_customer_id VARCHAR(5))
BEGIN
    SELECT
        OrderID,
        OrderDate,
        Freight
    FROM orders
    WHERE CustomerID = p_customer_id
    ORDER BY OrderDate, OrderID;
END$$

CREATE PROCEDURE sp_Top5ClientesCompradores()
BEGIN
    SELECT
        c.CustomerID,
        c.CompanyName,
        ROUND(SUM(od.Quantity * od.UnitPrice * (1 - od.Discount)), 2) AS TotalComprado
    FROM customers AS c
    INNER JOIN orders AS o
        ON o.CustomerID = c.CustomerID
    INNER JOIN order_details AS od
        ON od.OrderID = o.OrderID
    GROUP BY
        c.CustomerID,
        c.CompanyName
    ORDER BY TotalComprado DESC
    LIMIT 5;
END$$

DELIMITER ;

-- ============================================================
-- PARTE III: FUNCIONES
-- ============================================================

DROP FUNCTION IF EXISTS fn_TotalProductosCategoria;
DROP FUNCTION IF EXISTS fn_DescuentoProducto;

DELIMITER $$

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

-- ============================================================
-- PARTE IV: TRIGGERS
-- ============================================================

DROP TRIGGER IF EXISTS trg_clientes_validar_companyname;
DROP TRIGGER IF EXISTS trg_productos_eliminados;

CREATE TABLE IF NOT EXISTS productos_eliminados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    fecha_eliminacion DATETIME NOT NULL
);

DELIMITER $$

CREATE TRIGGER trg_clientes_validar_companyname
BEFORE INSERT ON customers
FOR EACH ROW
BEGIN
    IF NEW.CompanyName IS NULL OR TRIM(NEW.CompanyName) = '' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'El nombre de la empresa es obligatorio';
    END IF;
END$$

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

-- ============================================================
-- EJEMPLOS DE EJECUCION
-- ============================================================

-- CALL sp_ProductosProveedor('Exotic Liquids');
-- CALL sp_PedidosCliente('ALFKI');
-- SELECT fn_TotalProductosCategoria(1);
-- SELECT fn_DescuentoProducto(5);
-- CALL sp_Top5ClientesCompradores();
