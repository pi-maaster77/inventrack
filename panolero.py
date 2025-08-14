import sqlite3
import tkinter as tk
from tkinter import ttk

# Función para conectar a la base de datos y obtener los artículos
def obtener_articulos():
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('db')
    cursor = conn.cursor()
    
    # Consulta para obtener los artículos
    cursor.execute("SELECT nombre, descripcion, cantidad_total, cantidad_disponible FROM items")
    
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

# Crear la ventana principal de la aplicación
root = tk.Tk()
root.title("Artículos en Stock")

# Crear un marco para el Treeview
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

# Crear el Treeview para mostrar los artículos
tree = ttk.Treeview(frame, columns=("Nombre", "Descripción", "Cantidad Total", "Cantidad Disponible"), show="headings")
tree.pack()

# Configurar las columnas
tree.heading("Nombre", text="Nombre")
tree.heading("Descripción", text="Descripción")
tree.heading("Cantidad Total", text="Cantidad Total")
tree.heading("Cantidad Disponible", text="Cantidad Disponible")

# Establecer el ancho de las columnas
tree.column("Nombre", width=150)
tree.column("Descripción", width=250)
tree.column("Cantidad Total", width=100)
tree.column("Cantidad Disponible", width=150)

# Botón para cargar los artículos en el Treeview
boton_cargar = ttk.Button(root, text="Cargar Artículos", command=cargar_articulos)
boton_cargar.pack(pady=10)

# Ejecutar la interfaz gráfica
root.mainloop()
