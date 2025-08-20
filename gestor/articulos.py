from .db_manager import cursor, commit
import tkinter as tk
from tkinter import ttk, messagebox

def cargar_articulos(tree_articulos):
    for row in tree_articulos.get_children():
        tree_articulos.delete(row)
    cursor.execute("SELECT id, nombre, tipo_item, cantidad_disponible FROM items")
    for row in cursor.fetchall():
        tree_articulos.insert("", tk.END, values=row)

def agregar_articulo(entry_nombre, combo_tipo, entry_cantidad, tree_articulos):
    nombre = entry_nombre.get()
    tipo_item = combo_tipo.get()
    cantidad = entry_cantidad.get()

    if not nombre or not tipo_item or not cantidad:
        messagebox.showwarning("Campos vacíos", "Completa todos los campos")
        return

    try:
        cantidad = float(cantidad)
    except ValueError:
        messagebox.showerror("Error", "Cantidad debe ser un número")
        return

    cursor.execute(
        "INSERT INTO items (nombre, tipo_item, cantidad_total, cantidad_disponible) VALUES (?, ?, ?, ?)",
        (nombre, tipo_item, cantidad, cantidad))
    commit()
    cargar_articulos(tree_articulos)
    entry_nombre.delete(0, tk.END)
    entry_cantidad.delete(0, tk.END)

def editar_articulo(tree_articulos, root):
    selected = tree_articulos.focus()
    if not selected:
        messagebox.showwarning("Selecciona", "Debes seleccionar un artículo")
        return

    item_id, nombre, tipo, disponible = tree_articulos.item(selected, "values")

    def guardar_edicion():
        nuevo_nombre = edit_nombre.get()
        nuevo_tipo = edit_tipo.get()
        try:
            nueva_cantidad = float(edit_cantidad.get())
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un número")
            return

        cursor.execute("""
            UPDATE items 
            SET nombre=?, tipo_item=?, cantidad_total=?, cantidad_disponible=?
            WHERE id=?
        """, (nuevo_nombre, nuevo_tipo, nueva_cantidad, nueva_cantidad, item_id))
        commit()
        cargar_articulos(tree_articulos)
        ventana_editar.destroy()

    ventana_editar = tk.Toplevel(root)
    ventana_editar.title("Editar artículo")

    tk.Label(ventana_editar, text="Nombre:").grid(row=0, column=0)
    edit_nombre = tk.Entry(ventana_editar)
    edit_nombre.insert(0, nombre)
    edit_nombre.grid(row=0, column=1)

    tk.Label(ventana_editar, text="Tipo:").grid(row=1, column=0)
    edit_tipo = ttk.Combobox(ventana_editar, values=["Herramienta", "Recurso"], state="readonly")
    edit_tipo.set(tipo)
    edit_tipo.grid(row=1, column=1)

    tk.Label(ventana_editar, text="Cantidad:").grid(row=2, column=0)
    edit_cantidad = tk.Entry(ventana_editar)
    edit_cantidad.insert(0, disponible)
    edit_cantidad.grid(row=2, column=1)

    tk.Button(ventana_editar, text="Guardar", command=guardar_edicion).grid(row=3, column=0, columnspan=2, pady=10)

def eliminar_articulo(tree_articulos):
    selected = tree_articulos.focus()
    if not selected:
        messagebox.showwarning("Selecciona", "Debes seleccionar un artículo")
        return

    item_id, nombre, *_ = tree_articulos.item(selected, "values")
    if messagebox.askyesno("Confirmar", f"¿Eliminar el artículo '{nombre}'?"):
        cursor.execute("DELETE FROM items WHERE id=?", (item_id,))
        commit()
        cargar_articulos(tree_articulos)
