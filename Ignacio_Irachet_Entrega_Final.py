# Entrega final - Ignacio Irachet
# Gestor de inventario con base de datos SQLite
# Para que funcione hay que instalar colorama: pip install colorama

import sqlite3
from colorama import Fore, init

# con autoreset el color vuelve a la normalidad después de cada print
init(autoreset=True)

nombre_bd = "inventario.db"


# ----- Base de datos -----
def crear_base_datos():
    # crea la tabla productos si no existe
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                categoria TEXT
            )
        ''')
        conexion.commit()
        conexion.close()
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al crear la base de datos: {e}")


# ----- Funciones auxiliares -----
def pedir_entero(mensaje, minimo=0):
    # pide un número entero y vuelve a preguntar si está mal
    while True:
        try:
            valor = int(input(mensaje).strip())
            if valor < minimo:
                print(Fore.RED + f"Error: el valor debe ser {minimo} o mayor.")
            else:
                return valor
        except ValueError:
            print(Fore.RED + "Error: ingresá un número entero válido.")


def pedir_decimal(mensaje):
    # pide el precio y vuelve a preguntar si está mal
    while True:
        try:
            valor = float(input(mensaje).strip())
            if valor <= 0:
                print(Fore.RED + "Error: el precio debe ser mayor que cero.")
            else:
                return valor
        except ValueError:
            print(Fore.RED + "Error: ingresá un número válido, usando punto para los decimales (ej: 1500.50).")


def pedir_texto_obligatorio(mensaje):
    # pide un texto que no puede estar vacío
    while True:
        texto = input(mensaje).strip()
        if texto == "":
            print(Fore.RED + "Error: este campo no puede quedar vacío.")
        else:
            return texto


def mostrar_producto(producto):
    # muestra los datos de un producto
    print(f"ID: {producto[0]} | Nombre: {producto[1]} | Descripción: {producto[2]} | "
          f"Cantidad: {producto[3]} | Precio: ${producto[4]:.2f} | Categoría: {producto[5]}")


def obtener_producto_por_id(id_producto):
    # busca un producto por id (lo uso para actualizar y eliminar)
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        # uso ? para que la consulta sea segura (inyección SQL)
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
        producto = cursor.fetchone()
        conexion.close()
        return producto
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al consultar la base de datos: {e}")
        return None


# ----- Funcionalidades -----
def registrar_producto():
    # opción 1: agregar un producto nuevo
    print(Fore.YELLOW + "\n--- REGISTRAR PRODUCTO ---")
    nombre = pedir_texto_obligatorio("Nombre del producto: ").title()
    descripcion = input("Descripción (opcional): ").strip()
    cantidad = pedir_entero("Cantidad disponible: ")
    precio = pedir_decimal("Precio: ")
    categoria = input("Categoría (opcional): ").strip().title()

    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, descripcion, cantidad, precio, categoria))
        conexion.commit()
        conexion.close()
        print(Fore.GREEN + "Producto registrado correctamente.")
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al registrar el producto: {e}")


def ver_productos():
    # opción 2: mostrar todos los productos
    print(Fore.YELLOW + "\n--- PRODUCTOS REGISTRADOS ---")
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        conexion.close()

        if len(productos) == 0:
            print(Fore.RED + "No hay productos registrados.")
        else:
            for producto in productos:
                mostrar_producto(producto)
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al consultar los productos: {e}")


def actualizar_producto():
    # opción 3: modificar un producto con su id
    print(Fore.YELLOW + "\n--- ACTUALIZAR PRODUCTO ---")
    id_producto = pedir_entero("ID del producto a actualizar: ", 1)
    producto = obtener_producto_por_id(id_producto)

    if not producto:
        print(Fore.RED + "No existe un producto con ese ID.")
        return

    print("Producto actual:")
    mostrar_producto(producto)
    print("Dejá vacío el campo que no quieras modificar.")

    nuevo_nombre = input("Nuevo nombre: ").strip().title()
    nueva_descripcion = input("Nueva descripción: ").strip()
    nueva_cantidad = input("Nueva cantidad: ").strip()
    nuevo_precio = input("Nuevo precio: ").strip()
    nueva_categoria = input("Nueva categoría: ").strip().title()

    # si deja algo vacío queda el dato que ya estaba
    nombre = producto[1]
    descripcion = producto[2]
    cantidad = producto[3]
    precio = producto[4]
    categoria = producto[5]

    if nuevo_nombre != "":
        nombre = nuevo_nombre
    if nueva_descripcion != "":
        descripcion = nueva_descripcion
    if nueva_categoria != "":
        categoria = nueva_categoria

    # cantidad y precio tienen que ser números
    try:
        if nueva_cantidad != "":
            cantidad = int(nueva_cantidad)
        if nuevo_precio != "":
            precio = float(nuevo_precio)
    except ValueError:
        print(Fore.RED + "Error: cantidad o precio inválidos. No se modificó nada.")
        return

    if cantidad < 0 or precio <= 0:
        print(Fore.RED + "Error: la cantidad no puede ser negativa y el precio debe ser mayor que cero.")
        return

    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        cursor.execute('''
            UPDATE productos
            SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
            WHERE id = ?
        ''', (nombre, descripcion, cantidad, precio, categoria, id_producto))
        conexion.commit()
        conexion.close()
        print(Fore.GREEN + "Producto actualizado correctamente.")
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al actualizar el producto: {e}")


def buscar_producto():
    # opción 4: buscar por id, nombre o categoría
    print(Fore.YELLOW + "\n--- BUSCAR PRODUCTO ---")
    print("1. Buscar por ID")
    print("2. Buscar por nombre")
    print("3. Buscar por categoría")
    opcion = input("Elegí una opción: ").strip()

    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()

        if opcion == "1":
            id_producto = pedir_entero("ID a buscar: ", 1)
            cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
        elif opcion == "2":
            # uso title() porque así se guardan los nombres
            texto = input("Nombre a buscar: ").strip().title()
            cursor.execute("SELECT * FROM productos WHERE nombre = ?", (texto,))
        elif opcion == "3":
            texto = input("Categoría a buscar: ").strip().title()
            cursor.execute("SELECT * FROM productos WHERE categoria = ?", (texto,))
        else:
            print(Fore.RED + "Opción no válida.")
            conexion.close()
            return

        resultados = cursor.fetchall()
        conexion.close()

        if len(resultados) == 0:
            print(Fore.RED + "No se encontraron productos.")
        else:
            for producto in resultados:
                mostrar_producto(producto)
    except sqlite3.Error as e:
        print(Fore.RED + f"Error en la búsqueda: {e}")


def eliminar_producto():
    # opción 5: borrar un producto con su id (pide confirmación)
    print(Fore.YELLOW + "\n--- ELIMINAR PRODUCTO ---")
    id_producto = pedir_entero("ID del producto a eliminar: ", 1)
    producto = obtener_producto_por_id(id_producto)

    if not producto:
        print(Fore.RED + "No existe un producto con ese ID.")
        return

    mostrar_producto(producto)
    confirmacion = input("¿Seguro que querés eliminarlo? (s/n): ").strip().lower()

    if confirmacion == "s":
        try:
            conexion = sqlite3.connect(nombre_bd)
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
            conexion.commit()
            conexion.close()
            print(Fore.GREEN + "Producto eliminado correctamente.")
        except sqlite3.Error as e:
            print(Fore.RED + f"Error al eliminar el producto: {e}")
    else:
        print("Eliminación cancelada.")


def reporte_bajo_stock():
    # opción 6: productos con poco stock
    print(Fore.YELLOW + "\n--- REPORTE DE BAJO STOCK ---")
    limite = pedir_entero("Mostrar productos con cantidad igual o inferior a: ")

    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
        productos = cursor.fetchall()
        conexion.close()

        if len(productos) == 0:
            print(Fore.GREEN + f"No hay productos con cantidad igual o inferior a {limite}.")
        else:
            print(Fore.RED + f"Productos con cantidad igual o inferior a {limite}:")
            for producto in productos:
                mostrar_producto(producto)
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al generar el reporte: {e}")


# ----- Menú principal -----
def mostrar_menu():
    # muestra las opciones
    print(Fore.CYAN + "\n=== GESTOR DE INVENTARIO ===")
    print("1. Registrar producto")
    print("2. Ver productos")
    print("3. Actualizar producto")
    print("4. Buscar producto")
    print("5. Eliminar producto")
    print("6. Reporte de bajo stock")
    print("7. Salir")


def menu_principal():
    # el menú se repite hasta que se elige salir
    crear_base_datos()

    while True:
        mostrar_menu()
        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            ver_productos()
        elif opcion == "3":
            actualizar_producto()
        elif opcion == "4":
            buscar_producto()
        elif opcion == "5":
            eliminar_producto()
        elif opcion == "6":
            reporte_bajo_stock()
        elif opcion == "7":
            print(Fore.GREEN + "Gracias por usar el gestor de inventario.")
            break
        else:
            print(Fore.RED + "Opción no válida.")


# arranca el programa
menu_principal()
