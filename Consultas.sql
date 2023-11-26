SELECT * FROM Producto WHERE Precio > 100;
SELECT COUNT(*) FROM Producto WHERE Stock <= 10;
SELECT * FROM Producto WHERE Descripcion LIKE '%oferta%';
SELECT AVG(Precio) FROM Producto;
SELECT * FROM Producto WHERE Precio > 50;
SELECT COUNT(*) FROM Producto WHERE Stock <= 5;
SELECT * FROM Producto WHERE Descripcion LIKE '%descuento%';
SELECT AVG(Precio) FROM Producto WHERE Stock > 0;

SELECT U.Nombre AS NombreUsuario, C.Total AS TotalCarrito
FROM Usuario U
JOIN Carrito C ON U.ID = C.Usuario;

SELECT COUNT(DISTINCT U.ID) AS CantidadUsuarios
FROM Usuario U
JOIN Carrito C ON U.ID = C.Usuario
WHERE C.Total > 200;

SELECT U.Nombre AS NombreUsuario, C.Total AS TotalCarrito, O.Fecha AS FechaOrden
FROM Usuario U
JOIN Carrito C ON U.ID = C.Usuario
JOIN Ordenes O ON U.ID = O.Usuario;

SELECT COUNT(DISTINCT U.ID) AS CantidadUsuarios
FROM Usuario U
JOIN Carrito C ON U.ID = C.Usuario
JOIN Ordenes O ON U.ID = O.Usuario
WHERE C.Total > 200;

SELECT COUNT(DISTINCT U.ID) AS CantidadUsuarios
FROM Usuario U
JOIN Ordenes O ON U.ID = O.Usuario
JOIN Reviews_Producto RP ON U.ID = RP.Autor;

SELECT COUNT(DISTINCT U.ID) AS CantidadUsuarios
FROM Usuario U
JOIN Ordenes O ON U.ID = O.Usuario
JOIN Reviews_Producto RP ON U.ID = RP.Autor
JOIN Reviews_Vendedor RV ON U.ID = RV.Autor;

SELECT O.ID AS OrdenID, COUNT(LPO.ID_Producto) AS CantidadProductos
FROM Ordenes O
JOIN Lista_Productos_Orden LPO ON O.ID = LPO.ID_Orden
GROUP BY O.ID;

SELECT O.ID AS OrdenID, SUM(P.Precio) AS TotalOrden
FROM Ordenes O
JOIN Lista_Productos_Orden LPO ON O.ID = LPO.ID_Orden
JOIN Producto P ON LPO.ID_Producto = P.ID
GROUP BY O.ID;

SELECT U.ID AS UsuarioID, MAX(O.Fecha) AS UltimaOrdenFecha
FROM Usuario U
JOIN Ordenes O ON U.ID = O.Usuario
GROUP BY U.ID;

SELECT V.ID AS VendedorID, COUNT(O.ID) AS CantidadOrdenes
FROM Vendedor V
JOIN Producto P ON V.ID = P.Vendedor
JOIN Lista_Productos_Orden LPO ON P.ID = LPO.ID_Producto
JOIN Ordenes O ON LPO.ID_Orden = O.ID
GROUP BY V.ID;

SELECT O.ID AS OrdenID, MAX(P.Precio) AS PrecioMaximoPorOrden
FROM Ordenes O
JOIN Lista_Productos_Orden LPO ON O.ID = LPO.ID_Orden
JOIN Producto P ON LPO.ID_Producto = P.ID
GROUP BY O.ID;

SELECT V.ID AS VendedorID, SUM(P.Stock) AS TotalStockPorVendedor
FROM Vendedor V
JOIN Producto P ON V.ID = P.Vendedor
GROUP BY V.ID;

SELECT AVG(P.Precio) AS PrecioPromedioProductos
FROM Ordenes O
JOIN Lista_Productos_Orden LPO ON O.ID = LPO.ID_Orden
JOIN Producto P ON LPO.ID_Producto = P.ID;

SELECT V.ID AS VendedorID, SUM(P.Precio) AS TotalVentasPorVendedor
FROM Vendedor V
JOIN Producto P ON V.ID = P.Vendedor
JOIN Lista_Productos_Orden LPO ON P.ID = LPO.ID_Producto
JOIN Ordenes O ON LPO.ID_Orden = O.ID
GROUP BY V.ID;

SELECT U.Nombre AS NombreUsuario, C.Total AS TotalCarrito
FROM Usuario U
INNER JOIN Carrito C ON U.ID = C.Usuario;

SELECT P.Nombre AS NombreProducto, C.Categoria AS CategoriaProducto
FROM Producto P
INNER JOIN Categoria C ON P.ID = C.ID_Producto;

SELECT U.Nombre AS NombreUsuario, O.Fecha AS FechaOrden
FROM Usuario U
INNER JOIN Ordenes O ON U.ID = O.Usuario;

SELECT C.Categoria, COUNT(P.ID) AS CantidadProductos
FROM Categoria C
INNER JOIN Producto P ON C.ID_Producto = P.ID
GROUP BY C.Categoria;

SELECT U.Nombre AS NombreUsuario, C.Total AS TotalCarrito
FROM Usuario U
LEFT JOIN Carrito C ON U.ID = C.Usuario;

SELECT P.Nombre AS NombreProducto, C.Categoria AS CategoriaProducto
FROM Producto P
LEFT JOIN Categoria C ON P.ID = C.ID_Producto;

SELECT O.ID AS OrdenID, U.Nombre AS NombreUsuario, O.Fecha AS FechaOrden
FROM Ordenes O
LEFT JOIN Usuario U ON O.Usuario = U.ID;

SELECT * FROM Usuario
ORDER BY F_Creacion ASC;

SELECT Nombre AS NombreProducto, Precio
FROM Producto
ORDER BY Precio DESC;

SELECT U.Nombre AS NombreUsuario, C.Total AS TotalCarrito
FROM Usuario U
INNER JOIN Carrito C ON U.ID = C.Usuario
ORDER BY C.Total DESC;

SELECT P.Nombre AS NombreProducto, P.Cantidad_Vendida
FROM Producto P
ORDER BY P.Cantidad_Vendida DESC;

SELECT U.ID AS UsuarioID, U.Nombre AS NombreUsuario, SUM(P.Cantidad_Vendida) AS TotalProductosVendidos
FROM Usuario U
INNER JOIN Ordenes O ON U.ID = O.Usuario
INNER JOIN Lista_Productos_Orden LPO ON O.ID = LPO.ID_Orden
INNER JOIN Producto P ON LPO.ID_Producto = P.ID
GROUP BY U.ID, U.Nombre;

SELECT C.Categoria, SUM(P.Precio) AS TotalVentasPorCategoria
FROM Categoria C
INNER JOIN Producto P ON C.ID_Producto = P.ID
GROUP BY C.Categoria;

SELECT C.Categoria, AVG(P.Precio) AS PrecioPromedioPorCategoria
FROM Categoria C
INNER JOIN Producto P ON C.ID_Producto = P.ID
GROUP BY C.Categoria;

SELECT C.Categoria, SUM(P.Precio) AS TotalVentasPorCategoria
FROM Categoria C
INNER JOIN Producto P ON C.ID_Producto = P.ID
GROUP BY C.Categoria
HAVING TotalVentasPorCategoria > 1000;

SELECT P.Nombre AS NombreProducto, C.Categoria AS CategoriaProducto
FROM Producto P
INNER JOIN Lista_Productos_Carrito LPC ON P.ID = LPC.ID_Producto
LEFT JOIN Categoria C ON P.ID = C.ID_Producto;

SELECT U.Nombre AS NombreUsuario, C.Total AS TotalCarrito
FROM Usuario U
LEFT JOIN Carrito C ON U.ID = C.Usuario
LEFT JOIN Ordenes O ON U.ID = O.Usuario;

SELECT U.Nombre AS NombreUsuario, C.Total AS TotalCarrito
FROM Usuario U
INNER JOIN Carrito C ON U.ID = C.Usuario
LEFT JOIN Ordenes O ON U.ID = O.Usuario;

SELECT *
FROM Usuario
WHERE ID IN (
    SELECT DISTINCT Usuario
    FROM Ordenes
    WHERE Fecha > '2023-01-01'
);

SELECT *
FROM Producto
WHERE Precio > (
    SELECT AVG(Precio)
    FROM Producto
);

SELECT *
FROM Vendedor
WHERE ID IN (
    SELECT DISTINCT P.Vendedor
    FROM Producto P
    WHERE P.Stock > 0
);

SELECT U.Nombre AS NombreUsuario,
       (SELECT COUNT(*) FROM Ordenes O WHERE O.Usuario = U.ID) AS CantidadOrdenes
FROM Usuario U;

SELECT P.Nombre AS NombreProducto,
       P.Cantidad_Vendida,
       (SELECT SUM(Precio) FROM Producto WHERE ID = P.ID) AS TotalVentasPorProducto
FROM Producto P;

SELECT U.Nombre AS NombreUsuario,
       COALESCE((SELECT C.Total FROM Carrito C WHERE C.Usuario = U.ID), 'No tiene carrito') AS TotalCarrito
FROM Usuario U;

SELECT Nombre AS NombreProducto, NULL AS Categoria FROM Producto
UNION ALL
SELECT NULL, Categoria FROM Categoria;

SELECT Nombre FROM Usuario
UNION ALL
SELECT Ventas FROM Vendedor;

SELECT U.Nombre AS NombreUsuario, C.Total AS TotalCarrito, O.Fecha AS FechaOrden
FROM Usuario U
JOIN Carrito C ON U.ID = C.Usuario
JOIN Ordenes O ON U.ID = O.Usuario;

SELECT P.Nombre AS NombreProducto, C.Categoria AS CategoriaProducto
FROM Producto P
JOIN Categoria C ON P.ID = C.ID_Producto;

SELECT U.Nombre AS NombreUsuario,
       SUM(P.Cantidad_Vendida) AS TotalProductosVendidos
FROM Usuario U
JOIN Ordenes O ON U.ID = O.Usuario
JOIN Lista_Productos_Orden LPO ON O.ID = LPO.ID_Orden
JOIN Producto P ON LPO.ID_Producto = P.ID
GROUP BY U.ID, U.Nombre;
















