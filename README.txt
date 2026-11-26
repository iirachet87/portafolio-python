GESTOR DE INVENTARIO - Entrega final
Ignacio Irachet - Talento Tech, Iniciación a la programación con Python


DE QUÉ SE TRATA
Es un programa de consola para manejar el inventario de productos de un comercio.
Los datos se guardan en una base de datos SQLite (inventario.db), así que no se
pierden cuando se cierra el programa.


QUÉ HACE FALTA PARA USARLO
- Python 3
- El módulo colorama, que se instala con:
  pip install colorama


CÓMO SE EJECUTA
1. Abrir una terminal en la carpeta donde está el archivo.
2. Escribir:
   python Ignacio_Irachet_Entrega_Final.py
La primera vez se crea solo el archivo inventario.db con la tabla productos.


QUÉ SE PUEDE HACER (menú principal)
1. Registrar producto: pide nombre, descripción, cantidad, precio y categoría.
2. Ver productos: muestra todos los productos guardados.
3. Actualizar producto: se elige por ID y se cambian los datos. Si se deja un
   campo vacío, queda el dato que ya estaba.
4. Buscar producto: por ID, por nombre o por categoría.
5. Eliminar producto: se elige por ID y pide confirmación antes de borrar.
6. Reporte de bajo stock: muestra los productos con cantidad igual o menor
   al número que ingresa el usuario.
7. Salir


TABLA productos
id           entero, clave primaria, autoincremental
nombre       texto, no puede ser nulo
descripcion  texto
cantidad     entero, no puede ser nulo
precio       real, no puede ser nulo
categoria    texto


EJEMPLO DE USO
=== GESTOR DE INVENTARIO ===
1. Registrar producto
2. Ver productos
3. Actualizar producto
4. Buscar producto
5. Eliminar producto
6. Reporte de bajo stock
7. Salir
Elegí una opción: 6

--- REPORTE DE BAJO STOCK ---
Mostrar productos con cantidad igual o inferior a: 5
Productos con cantidad igual o inferior a 5:
ID: 2 | Nombre: Mouse | Descripción:  | Cantidad: 3 | Precio: $8000.00 | Categoría: Perifericos


OTRAS COSAS
- Se validan los datos que se ingresan (no se aceptan campos obligatorios vacíos,
  ni letras donde van números, ni precios en cero o negativos).
- Las consultas a la base usan parámetros (?) para evitar inyección SQL.
- Se usa try-except para manejar los errores de la base de datos.
- Los precios con decimales se escriben con punto (ej: 1500.50).
