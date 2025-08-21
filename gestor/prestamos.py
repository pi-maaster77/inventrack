from .db_manager import cursor, commit
import tkinter as tk
from tkinter import ttk, messagebox

def cargar_prestamos(tree_prestamos):
    for row in tree_prestamos.get_children():
        tree_prestamos.delete(row)
    cursor.execute("""
        SELECT p.id, p.persona_id, pe.nombre || ' ' || pe.apellido, p.fecha_prestamo, p.vigente
        FROM prestamos p
        JOIN personas pe ON pe.dni = p.persona_id
    """)
    for row in cursor.fetchall():
        tree_prestamos.insert("", tk.END, values=row)

def registrar_prestamo(entry_persona_id, tree_prestamos):
    persona_id = entry_persona_id.get()
    if not persona_id:
        messagebox.showwarning("Error", "Debe ingresar el DNI de la persona")
        return

    try:
        cursor.execute("INSERT INTO prestamos (persona_id) VALUES (?)", (persona_id,))
        commit()
        cargar_prestamos(tree_prestamos)
        entry_persona_id.delete(0, tk.END)
    except Exception:
        messagebox.showerror("Error", "Persona no encontrada o error de integridad")

def devolver_prestamo(tree_prestamos):
    selected = tree_prestamos.focus()
    if not selected:
        messagebox.showwarning("Selecciona", "Debes seleccionar un préstamo")
        return

    prestamo_id, *_ = tree_prestamos.item(selected, "values")

    if messagebox.askyesno("Confirmar", f"¿Registrar devolución del préstamo #{prestamo_id}?"):
        cursor.execute("""
            SELECT item_id, cantidad FROM detalle_prestamo_item WHERE prestamo_id=?
        """, (prestamo_id,))
        for item_id, cantidad in cursor.fetchall():
            cursor.execute("""
                UPDATE items 
                SET cantidad_disponible = cantidad_disponible + ?
                WHERE id=?
            """, (cantidad, item_id))
        cursor.execute("UPDATE prestamos SET vigente=0, fecha_devolucion=DATE('now') WHERE id=?", (prestamo_id,))
        commit()
        cargar_prestamos(tree_prestamos)

def ver_detalle_prestamo(event, tree_prestamos, root):
    def actualizar_detalle():
        # Limpiar y recargar la tabla de detalles
        for row in tree_detalle.get_children():
            tree_detalle.delete(row)
        cursor.execute("""
            SELECT dpi.id, i.nombre, dpi.cantidad, dpi.condicion
            FROM detalle_prestamo_item dpi
            JOIN items i ON dpi.item_id = i.id
            WHERE dpi.prestamo_id = ?
        """, (prestamo_id,))
        for row in cursor.fetchall():
            tree_detalle.insert("", tk.END, values=row)
        # Repetir cada 5 segundos
        detalle_window.after(5000, actualizar_detalle)

    def actualizar_prestamos():
        cargar_prestamos(tree_prestamos)
        tree_prestamos.after(5000, actualizar_prestamos)

    selected_item = tree_prestamos.focus()
    if not selected_item:
        return

    datos = tree_prestamos.item(selected_item, "values")
    prestamo_id = datos[0]

    detalle_window = tk.Toplevel(root)
    detalle_window.title(f"Detalle del Préstamo #{prestamo_id}")
    detalle_window.geometry("750x480")
    detalle_window.configure(bg="#f4f6fa")

    tk.Label(detalle_window, text=f"Detalles del Préstamo ID {prestamo_id}", font=("Segoe UI", 15, "bold"), bg="#f4f6fa", fg="#007bff").pack(pady=10)

    frame_tabla = tk.Frame(detalle_window, bg="#f4f6fa")
    frame_tabla.pack(expand=True, fill="both", padx=20, pady=10)

    tree_detalle = ttk.Treeview(frame_tabla, columns=("ID", "Artículo", "Cantidad", "Condición"), show="headings", height=12)
    for col in ("ID", "Artículo", "Cantidad", "Condición"):
        tree_detalle.heading(col, text=col)
    tree_detalle.pack(side="left", expand=True, fill="both")

    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree_detalle.yview)
    tree_detalle.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    actualizar_detalle()
    actualizar_prestamos()

    edit_frame = tk.Frame(detalle_window, bg="#f4f6fa")
    edit_frame.pack(fill="x", pady=10)

    tk.Label(edit_frame, text="Gestión de detalles del préstamo", font=("Segoe UI", 12, "bold"), bg="#f4f6fa", fg="#007bff").pack(pady=(0,5))

    def editar_condicion(event):
        selected = tree_detalle.focus()
        if not selected:
            return
        valores = tree_detalle.item(selected, "values")
        detalle_id, articulo, cantidad, condicion = valores

        edit_win = tk.Toplevel(detalle_window)
        edit_win.title(f"Modificar detalle - {articulo}")
        edit_win.geometry("340x220")
        edit_win.configure(bg="#f4f6fa")

        tk.Label(edit_win, text=f"Artículo: {articulo}", font=("Segoe UI", 11), bg="#f4f6fa").grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(edit_win, text="Cantidad:", font=("Segoe UI", 11), bg="#f4f6fa").grid(row=1, column=0, sticky="e")
        entry_cantidad = tk.Entry(edit_win, font=("Segoe UI", 11), width=12)
        entry_cantidad.insert(0, cantidad)
        entry_cantidad.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(edit_win, text="Condición:", font=("Segoe UI", 11), bg="#f4f6fa").grid(row=2, column=0, sticky="e")
        combo_cond = ttk.Combobox(edit_win, values=list(range(0, 11)), state="readonly", font=("Segoe UI", 11), width=10)
        combo_cond.set(condicion if condicion is not None else 0)
        combo_cond.grid(row=2, column=1, padx=10, pady=5)

        def guardar():
            try:
                nueva_cantidad = float(entry_cantidad.get())
            except ValueError:
                messagebox.showerror("Error", "Cantidad debe ser un número")
                return
            nueva_cond = int(combo_cond.get())
            # Actualizar cantidad y condición
            cursor.execute("SELECT item_id FROM detalle_prestamo_item WHERE id=?", (detalle_id,))
            item_id = cursor.fetchone()[0]
            # Obtener cantidad anterior
            cursor.execute("SELECT cantidad FROM detalle_prestamo_item WHERE id=?", (detalle_id,))
            cantidad_ant = cursor.fetchone()[0]
            # Ajustar stock si cambia cantidad
            if nueva_cantidad != cantidad_ant:
                diff = nueva_cantidad - cantidad_ant
                cursor.execute("SELECT cantidad_disponible FROM items WHERE id=?", (item_id,))
                disponible = cursor.fetchone()[0]
                if diff > 0 and diff > disponible:
                    messagebox.showerror("Error", "No hay suficiente stock disponible para aumentar la cantidad")
                    return
                cursor.execute("UPDATE items SET cantidad_disponible = cantidad_disponible - ? WHERE id=?", (diff, item_id))
            cursor.execute("UPDATE detalle_prestamo_item SET cantidad=?, condicion=? WHERE id=?", (nueva_cantidad, nueva_cond, detalle_id))
            commit()
            tree_detalle.item(selected, values=(detalle_id, articulo, nueva_cantidad, nueva_cond))
            edit_win.destroy()

            cursor.execute("SELECT COUNT(*) FROM detalle_prestamo_item WHERE prestamo_id=? AND (condicion=0 OR condicion IS NULL)", (prestamo_id,))
            pendientes = cursor.fetchone()[0]
            if pendientes == 0:
                cursor.execute("UPDATE prestamos SET vigente=0, fecha_devolucion=DATE('now') WHERE id=?", (prestamo_id,))
                commit()
                cargar_prestamos(tree_prestamos)

        ttk.Button(edit_win, text="Guardar cambios", command=guardar).grid(row=3, column=0, columnspan=2, pady=18)

    tree_detalle.bind("<Double-1>", editar_condicion)

    # --- Agregar y quitar ítems prestados ---
    def agregar_item_prestado():
        win = tk.Toplevel(detalle_window)
        win.title("Agregar ítem al préstamo")
        win.geometry("370x180")
        win.configure(bg="#f4f6fa")

        tk.Label(win, text="Artículo:", font=("Segoe UI", 11), bg="#f4f6fa").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        # Obtener lista de artículos disponibles
        cursor.execute("SELECT id, nombre FROM items WHERE cantidad_disponible > 0")
        items = cursor.fetchall()
        item_ids = [str(i[0]) for i in items]
        item_names = [i[1] for i in items]
        combo_item = ttk.Combobox(win, values=item_names, state="readonly", font=("Segoe UI", 11), width=20)
        combo_item.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(win, text="Cantidad:", font=("Segoe UI", 11), bg="#f4f6fa").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        entry_cantidad = tk.Entry(win, font=("Segoe UI", 11), width=12)
        entry_cantidad.grid(row=1, column=1, padx=10, pady=10)

        def guardar_item():
            nombre = combo_item.get()
            cantidad = entry_cantidad.get()
            if not nombre or not cantidad:
                messagebox.showwarning("Campos vacíos", "Completa todos los campos")
                return
            try:
                cantidad = float(cantidad)
            except ValueError:
                messagebox.showerror("Error", "Cantidad debe ser un número")
                return
            # Buscar el id del artículo
            idx = item_names.index(nombre)
            item_id = int(item_ids[idx])
            # Verificar stock
            cursor.execute("SELECT cantidad_disponible FROM items WHERE id=?", (item_id,))
            disponible = cursor.fetchone()[0]
            if cantidad > disponible:
                messagebox.showerror("Error", "No hay suficiente stock disponible")
                return
            # Insertar detalle
            cursor.execute("INSERT INTO detalle_prestamo_item (prestamo_id, item_id, cantidad, condicion) VALUES (?, ?, ?, 0)", (prestamo_id, item_id, cantidad))
            cursor.execute("UPDATE items SET cantidad_disponible = cantidad_disponible - ? WHERE id=?", (cantidad, item_id))
            commit()
            # Actualizar tabla
            tree_detalle.insert("", tk.END, values=(cursor.lastrowid, nombre, cantidad, 0))
            win.destroy()

        ttk.Button(win, text="Agregar", command=guardar_item).grid(row=2, column=0, columnspan=2, pady=18)

    def quitar_item_prestado():
        selected = tree_detalle.focus()
        if not selected:
            messagebox.showwarning("Selecciona", "Debes seleccionar un ítem")
            return
        valores = tree_detalle.item(selected, "values")
        detalle_id, articulo, cantidad, condicion = valores
        if messagebox.askyesno("Confirmar", f"¿Quitar el artículo '{articulo}' del préstamo?"):
            # Devolver cantidad al stock
            cursor.execute("SELECT item_id FROM detalle_prestamo_item WHERE id=?", (detalle_id,))
            item_id = cursor.fetchone()[0]
            cursor.execute("UPDATE items SET cantidad_disponible = cantidad_disponible + ? WHERE id=?", (cantidad, item_id))
            # Eliminar detalle
            cursor.execute("DELETE FROM detalle_prestamo_item WHERE id=?", (detalle_id,))
            commit()
            tree_detalle.delete(selected)

    btn_agregar = ttk.Button(edit_frame, text="Agregar ítem", command=agregar_item_prestado)
    btn_agregar.pack(side="left", padx=8)
    btn_quitar = ttk.Button(edit_frame, text="Quitar ítem", command=quitar_item_prestado)
    btn_quitar.pack(side="left", padx=8)
