import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_PATH = "db"  # Cambia esto si tu DB está en otra ruta


def conectar():
    return sqlite3.connect(DB_PATH)


def obtener_columnas(tabla):
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute(f"PRAGMA table_info({tabla})")
        return cur.fetchall()


def obtener_datos(tabla):
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {tabla}")
        return cur.fetchall()


def insertar_registro(tabla, valores):
    columnas = [col[1] for col in obtener_columnas(tabla) if col[5] == 0]
    placeholders = ", ".join("?" for _ in columnas)
    sql = f"INSERT INTO {tabla} ({', '.join(columnas)}) VALUES ({placeholders})"

    with conectar() as conn:
        cur = conn.cursor()
        cur.execute(sql, valores)
        conn.commit()


def actualizar_registro(tabla, valores, id_col, id_val):
    columnas = [col[1] for col in obtener_columnas(tabla) if col[1] != id_col]
    sets = ", ".join(f"{col}=?" for col in columnas)
    sql = f"UPDATE {tabla} SET {sets} WHERE {id_col}=?"

    with conectar() as conn:
        cur = conn.cursor()
        cur.execute(sql, valores + [id_val])
        conn.commit()


def eliminar_registro(tabla, id_col, id_val):
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {tabla} WHERE {id_col}=?", (id_val,))
        conn.commit()


def mostrar_formulario(tabla, columnas, callback, valores_iniciales=None):
    ventana = tk.Toplevel()
    ventana.title("Formulario")

    entradas = {}
    row_index = 0
    for col in columnas:
        col_id, col_nombre, _, _, _, es_pk = col
        if es_pk:  # No permitir editar clave primaria
            continue

        ttk.Label(ventana, text=col_nombre).grid(row=row_index, column=0, sticky="w")
        entry = ttk.Entry(ventana)
        entry.grid(row=row_index, column=1)
        if valores_iniciales:
            idx = [c[1] for c in columnas].index(col_nombre)
            entry.insert(0, valores_iniciales[idx])
        entradas[col_nombre] = entry
        row_index += 1

    def enviar():
        try:
            valores = [entry.get() for entry in entradas.values()]
            callback(valores)
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ttk.Button(ventana, text="Guardar", command=enviar).grid(row=row_index, columnspan=2, pady=10)


def crear_ventana_para_tabla(tabla):
    ventana = tk.Toplevel()
    ventana.title(f"Gestión de: {tabla}")

    columnas = obtener_columnas(tabla)
    nombres_columnas = [col[1] for col in columnas]

    tree = ttk.Treeview(ventana, columns=nombres_columnas, show="headings", height=15)
    for nombre in nombres_columnas:
        tree.heading(nombre, text=nombre)
        tree.column(nombre, width=120)
    tree.pack(pady=10, fill="x", expand=True)

    def recargar():
        for i in tree.get_children():
            tree.delete(i)
        for fila in obtener_datos(tabla):
            tree.insert("", "end", values=fila)

    recargar()

    def agregar():
        mostrar_formulario(tabla, columnas, lambda valores: (insertar_registro(tabla, valores), recargar()))

    def editar():
        item = tree.focus()
        if not item:
            messagebox.showwarning("Selecciona", "Selecciona un registro para editar.")
            return

        valores = tree.item(item)["values"]
        id_col = [col[1] for col in columnas if col[5]][0]
        id_val = valores[[col[1] for col in columnas].index(id_col)]

        def callback_edit(valores_editados):
            actualizar_registro(tabla, valores_editados, id_col, id_val)
            recargar()

        mostrar_formulario(tabla, columnas, callback_edit, valores)

    def eliminar():
        item = tree.focus()
        if not item:
            messagebox.showwarning("Selecciona", "Selecciona un registro para eliminar.")
            return

        valores = tree.item(item)["values"]
        id_col = [col[1] for col in columnas if col[5]][0]
        id_val = valores[[col[1] for col in columnas].index(id_col)]

        if messagebox.askyesno("Confirmar", f"¿Eliminar el registro {id_val}?"):
            eliminar_registro(tabla, id_col, id_val)
            recargar()

    frame_botones = ttk.Frame(ventana)
    frame_botones.pack(pady=5)

    ttk.Button(frame_botones, text="Agregar", command=agregar).pack(side="left", padx=5)
    ttk.Button(frame_botones, text="Editar", command=editar).pack(side="left", padx=5)
    ttk.Button(frame_botones, text="Eliminar", command=eliminar).pack(side="left", padx=5)


def crear_selector_tabla():
    root = tk.Tk()
    root.title("Gestor de Base de Datos SQLite")

    ttk.Label(root, text="Selecciona una tabla:").pack(pady=10)

    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas = [fila[0] for fila in cur.fetchall()]

    combo = ttk.Combobox(root, values=tablas, state="readonly")
    combo.pack(pady=5)

    def abrir_tabla():
        tabla = combo.get()
        if tabla:
            crear_ventana_para_tabla(tabla)

    ttk.Button(root, text="Abrir", command=abrir_tabla).pack(pady=5)
    root.mainloop()


if __name__ == "__main__":
    crear_selector_tabla()
