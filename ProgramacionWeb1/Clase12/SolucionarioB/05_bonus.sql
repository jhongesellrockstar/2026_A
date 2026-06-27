USE northwind;

DROP PROCEDURE IF EXISTS sp_Top5ClientesCompradores;

DELIMITER $$

-- Pregunta bonus
-- Muestra los 5 clientes con mayor monto comprado.
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

-- Ejemplo:
-- CALL sp_Top5ClientesCompradores();
