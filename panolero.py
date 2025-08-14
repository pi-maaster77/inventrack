import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Función para conectar a la base de datos y obtener los artículos
def obtener_articulos():
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('db')  # Asegúrate de que 'db' sea tu archivo de base de datos
    cursor = conn.cursor()
    
    # Consulta para obtener todos los campos de los artículos, incluyendo cantidad disponible calculada
    cursor.execute("""
        SELECT 
            items.id,
            items.nombre, 
            items.descripcion, 
            items.cantidad_total, 
            IFNULL(SUM(detalle_prestamo_item.cantidad), 0) AS cantidad_prestada,
            (items.cantidad_total - IFNULL(SUM(detalle_prestamo_item.cantidad), 0)) AS cantidad_disponible,
            items.categoria_id, 
            items.ubicacion_id, 
            items.tipo_item
        FROM items
        LEFT JOIN detalle_prestamo_item ON detalle_prestamo_item.item_id = items.id
        GROUP BY items.id
    """)
    
    # Obtener todos los resultados
    articulos = cursor.fetchall()
    
    # Cerrar la conexión
    conn.close()
    
    return articulos

# Función para cargar los artículos en el Treeview
def cargar_articulos():
    # Limpiar el Treeview antes de cargar nuevos datos
    for item in tree.get_children():
        tree.delete(item)
    
    # Obtener los artículos de la base de datos
    articulos = obtener_articulos()
    
    # Insertar los artículos en el Treeview
    for articulo in articulos:
        tree.insert('', 'end', values=articulo)

# Función para agregar un nuevo artículo (ventana emergente)
def agregar_item():
    # Crear la nueva ventana
    ventana_agregar = tk.Toplevel()
    ventana_agregar.title("Agregar Nuevo Artículo")
    
    # Etiquetas y campos de entrada para el nuevo artículo
    ttk.Label(ventana_agregar, text="Nombre:").grid(row=0, column=0, sticky="w")
    entry_nombre = ttk.Entry(ventana_agregar)
    entry_nombre.grid(row=0, column=1)

    ttk.Label(ventana_agregar, text="Descripción:").grid(row=1, column=0, sticky="w")
    entry_descripcion = ttk.Entry(ventana_agregar)
    entry_descripcion.grid(row=1, column=1)

    ttk.Label(ventana_agregar, text="Cantidad Total:").grid(row=2, column=0, sticky="w")
    entry_cantidad_total = ttk.Entry(ventana_agregar)
    entry_cantidad_total.grid(row=2, column=1)

    ttk.Label(ventana_agregar, text="Cantidad Disponible:").grid(row=3, column=0, sticky="w")
    entry_cantidad_disponible = ttk.Entry(ventana_agregar)
    entry_cantidad_disponible.grid(row=3, column=1)

    ttk.Label(ventana_agregar, text="Categoría ID:").grid(row=4, column=0, sticky="w")
    entry_categoria_id = ttk.Entry(ventana_agregar)
    entry_categoria_id.grid(row=4, column=1)

    ttk.Label(ventana_agregar, text="Ubicación ID:").grid(row=5, column=0, sticky="w")
    entry_ubicacion_id = ttk.Entry(ventana_agregar)
    entry_ubicacion_id.grid(row=5, column=1)

    ttk.Label(ventana_agregar, text="Tipo de Artículo:").grid(row=6, column=0, sticky="w")
    entry_tipo_item = ttk.Entry(ventana_agregar)
    entry_tipo_item.grid(row=6, column=1)

    # Función para agregar el artículo a la base de datos y cerrar la ventana emergente
    def agregar():
        nombre = entry_nombre.get()
        descripcion = entry_descripcion.get()
        cantidad_total = entry_cantidad_total.get()
        cantidad_disponible = entry_cantidad_disponible.get()
        categoria_id = entry_categoria_id.get()
        ubicacion_id = entry_ubicacion_id.get()
        tipo_item = entry_tipo_item.get()

        # Validación de campos vacíos
        if not nombre or not descripcion or not cantidad_total or not cantidad_disponible or not categoria_id or not ubicacion_id or not tipo_item:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            # Convertir las cantidades a números
            cantidad_total = float(cantidad_total)
            cantidad_disponible = float(cantidad_disponible)

            # Conectar a la base de datos para agregar el nuevo artículo
            conn = sqlite3.connect('db')
            cursor = conn.cursor()

            # Insertar el nuevo artículo en la base de datos
            cursor.execute("""
                INSERT INTO items (nombre, descripcion, cantidad_total, cantidad_disponible, categoria_id, ubicacion_id, tipo_item) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (nombre, descripcion, cantidad_total, cantidad_disponible, categoria_id, ubicacion_id, tipo_item))

            # Guardar cambios y cerrar la conexión
            conn.commit()
            conn.close()

            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", "Artículo agregado correctamente")

            # Cargar nuevamente los artículos en el Treeview
            cargar_articulos()

            # Cerrar la ventana emergente
            ventana_agregar.destroy()

        except ValueError:
            messagebox.showerror("Error", "Las cantidades y los IDs deben ser números")

    # Botón para agregar el artículo
    boton_agregar = ttk.Button(ventana_agregar, text="Agregar Artículo", command=agregar)
    boton_agregar.grid(row=7, columnspan=2, pady=10)

# Crear la ventana principal de la aplicación
root = tk.Tk()
root.title("Artículos en Stock")

# Crear un marco para el Treeview
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

# Crear el Treeview para mostrar los artículos
tree = ttk.Treeview(frame, columns=("ID", "Nombre", "Descripción", "Cantidad Total", "Cantidad Disponible", "Categoría ID", "Ubicación ID", "Tipo de Artículo"), show="headings")
tree.pack()

# Configurar las columnas
tree.heading("ID", text="ID")
tree.heading("Nombre", text="Nombre")
tree.heading("Descripción", text="Descripción")
tree.heading("Cantidad Total", text="Cantidad Total")
tree.heading("Cantidad Disponible", text="Cantidad Disponible")
tree.heading("Categoría ID", text="Categoría ID")
tree.heading("Ubicación ID", text="Ubicación ID")
tree.heading("Tipo de Artículo", text="Tipo de Artículo")

# Establecer el ancho de las columnas
tree.column("ID", width=50)
tree.column("Nombre", width=150)
tree.column("Descripción", width=250)
tree.column("Cantidad Total", width=100)
tree.column("Cantidad Disponible", width=150)
tree.column("Categoría ID", width=100)
tree.column("Ubicación ID", width=100)
tree.column("Tipo de Artículo", width=150)

# Botón para cargar los artículos en el Treeview
boton_cargar = ttk.Button(root, text="Cargar Artículos", command=cargar_articulos)
boton_cargar.pack(pady=10)

# Botón para abrir la ventana emergente para agregar artículos
boton_agregar = ttk.Button(root, text="Agregar Artículo", command=agregar_item)
boton_agregar.pack(pady=10)

# Ejecutar la interfaz gráfica
root.mainloop()
