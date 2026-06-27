USE northwind;

-- Pregunta 1
-- Productos con stock superior al stock promedio.
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
-- Cinco proveedores que suministran la mayor cantidad de productos.
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
-- Total de ventas realizadas por cada empleado.
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
-- Categorias con mas de 10 productos registrados.
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
