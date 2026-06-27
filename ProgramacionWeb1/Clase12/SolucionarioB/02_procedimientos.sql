USE northwind;

DROP PROCEDURE IF EXISTS sp_ProductosProveedor;
DROP PROCEDURE IF EXISTS sp_PedidosCliente;

DELIMITER $$

-- Pregunta 5
-- Muestra todos los productos suministrados por un proveedor.
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

-- Pregunta 6
-- Muestra todos los pedidos realizados por un cliente.
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

DELIMITER ;

-- Ejemplos:
-- CALL sp_ProductosProveedor('Exotic Liquids');
-- CALL sp_PedidosCliente('ALFKI');
