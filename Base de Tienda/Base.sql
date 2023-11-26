CREATE TABLE [Usuario](
  [ID] INTEGER PRIMARY KEY AUTOINCREMENT, 
  [Nombre] VARCHAR(100), 
  [Email] VARCHAR(100), 
  [Password] INTEGER, 
  [F_Creacion] DATE);

CREATE TABLE [Carrito](
  [ID] INTEGER PRIMARY KEY AUTOINCREMENT, 
  [Usuario] INTEGER REFERENCES [Usuario]([ID]), 
  [Total] INTEGER);

CREATE TABLE [Vendedor](
  [ID] INTEGER PRIMARY KEY AUTOINCREMENT, 
  [Ventas] INTEGER, 
  [ID_Usuario] INTEGER REFERENCES [Usuario]([ID]));

CREATE TABLE [Producto](
  [ID] INTEGER PRIMARY KEY AUTOINCREMENT, 
  [Nombre] VARCHAR(100), 
  [Descripcion] TEXT, 
  [Descripcion_Larga] TEXT, 
  [Vendedor] INTEGER REFERENCES [Vendedor]([ID]), 
  [Marca] VARCHAR, 
  [Stock] INTEGER, 
  [F_Publicacion] DATE, 
  [Cantidad_Vendida] INTEGER, 
  [Precio] DOUBLE);

CREATE TABLE [Categoria](
  [ID_Producto] INTEGER REFERENCES [Producto]([ID]), 
  [Categoria] VARCHAR);

CREATE TABLE [Imagenes_Producto](
  [ID_Producto] INTEGER REFERENCES [Producto]([ID]), 
  [Imagen] IMAGE);

CREATE TABLE [Lista_Productos_Carrito](
  [ID_Carrito] INTEGER REFERENCES [Carrito]([ID]), 
  [ID_Producto] INTEGER REFERENCES [Producto]([ID]));

CREATE TABLE [Ordenes](
  [ID] INTEGER PRIMARY KEY AUTOINCREMENT, 
  [Fecha] DATE, 
  [Total] INTEGER, 
  [Usuario] INTEGER REFERENCES [Usuario]([ID]), 
  [Vendedor] INTEGER REFERENCES [Vendedor]([ID]));

CREATE TABLE [Lista_Productos_Orden](
  [ID_Orden] INTEGER REFERENCES [Ordenes]([ID]), 
  [ID_Producto] INTEGER REFERENCES [Producto]([ID]));

CREATE TABLE [Lista_Productos_Vendedor](
  [ID_Vendedor] INTEGER REFERENCES [Vendedor]([ID]), 
  [ID_Producto] INTEGER REFERENCES [Producto]([ID]));

CREATE TABLE [Preguntas](
  [ID] INTEGER PRIMARY KEY AUTOINCREMENT, 
  [Titulo] VARCHAR, 
  [Contenido] TEXT, 
  [Fecha] DATE, 
  [Autor] INTEGER REFERENCES [Usuario]([ID]), 
  [Producto] INTEGER REFERENCES [Producto]([ID]));

CREATE TABLE "Reviews_Producto"(
  [ID] INTEGER PRIMARY KEY AUTOINCREMENT, 
  [Titulo] VARCHAR, 
  [Contenido] TEXT, 
  [Fecha] DATE, 
  [Calificacion] INTEGER, 
  [Autor] INTEGER REFERENCES [Usuario]([ID]), 
  [Producto] INTEGER REFERENCES [Producto]([ID]));

CREATE TABLE [Reviews_Vendedor](
  [ID] INTEGER PRIMARY KEY AUTOINCREMENT, 
  [Titulo] VARCHAR, 
  [Contenido] TEXT, 
  [Fecha] DATE, 
  [Calificacion] INTEGER, 
  [Autor] INTEGER REFERENCES [Usuario]([ID]), 
  [Vendedor] INTEGER REFERENCES [Vendedor]([ID]));

CREATE VIEW Ordenes_Actuales AS
SELECT Fecha, Usuario, Total
FROM Ordenes;

CREATE VIEW Productos_Stock AS
SELECT Nombre, Stock, Precio
FROM Producto;

CREATE VIEW VistaCarrito AS
SELECT
    U.Nombre AS NombreUsuario,
    C.ID AS ID_Carrito,
    C.Total AS TotalCarrito
FROM
    Carrito C
JOIN
    Usuario U ON U.ID = C.Usuario;

