import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from .articulos import cargar_articulos, agregar_articulo, editar_articulo, eliminar_articulo
from .prestamos import cargar_prestamos, registrar_prestamo, devolver_prestamo, ver_detalle_prestamo
from .httppath import httppath
def run_app():
    root = tk.Tk()
    root.title("Administrador de Pañol")
    root.geometry("950x650")
    root.configure(bg="#f4f6fa")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TNotebook", background="#e9ecef", borderwidth=0)
    style.configure("TFrame", background="#f4f6fa")
    style.configure("Treeview", font=("Segoe UI", 11), rowheight=28, fieldbackground="#ffffff", background="#ffffff", foreground="#222")
    style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#dee2e6", foreground="#222")
    style.map("Treeview", background=[("selected", "#cce5ff")], foreground=[("selected", "#222")])
    style.configure("TButton", font=("Segoe UI", 11), padding=6, background="#007bff", foreground="#fff")
    style.map("TButton", background=[("active", "#0056b3")])
    style.configure("TLabel", font=("Segoe UI", 11), background="#f4f6fa")


    tabs = ttk.Notebook(root)
    tabs.pack(expand=True, fill="both")

    # TAB ARTÍCULOS
    frame_articulos = ttk.Frame(tabs)
    tabs.add(frame_articulos, text="Artículos")

    tree_articulos = ttk.Treeview(frame_articulos, columns=("ID", "Nombre", "Tipo", "Disponible"), show="headings")
    for col in ("ID", "Nombre", "Tipo", "Disponible"):
        tree_articulos.heading(col, text=col)
    tree_articulos.pack(expand=True, fill="both", padx=20, pady=20)

    # Etiqueta de título
    lbl_titulo = tk.Label(frame_articulos, text="Gestión de Artículos", font=("Segoe UI", 16, "bold"), bg="#f4f6fa", fg="#007bff")
    lbl_titulo.pack(pady=(10,0))

    def abrir_ventana_agregar():
        from tkinter import messagebox
        ventana_agregar = tk.Toplevel(root)
        ventana_agregar.title("Agregar artículo")
        ventana_agregar.geometry("400x220")
        ventana_agregar.configure(bg="#f4f6fa")

        tk.Label(ventana_agregar, text="Nombre:", font=("Segoe UI", 11), bg="#f4f6fa").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        entry_nombre = tk.Entry(ventana_agregar, font=("Segoe UI", 11), width=22)
        entry_nombre.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(ventana_agregar, text="Tipo:", font=("Segoe UI", 11), bg="#f4f6fa").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        combo_tipo = ttk.Combobox(ventana_agregar, values=["Herramienta", "Recurso"], state="readonly", font=("Segoe UI", 11), width=20)
        combo_tipo.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(ventana_agregar, text="Cantidad:", font=("Segoe UI", 11), bg="#f4f6fa").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        entry_cantidad = tk.Entry(ventana_agregar, font=("Segoe UI", 11), width=22)
        entry_cantidad.grid(row=2, column=1, padx=10, pady=10)

        # Imagen
        tk.Label(ventana_agregar, text="Imagen:", font=("Segoe UI", 11), bg="#f4f6fa").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        entry_img = tk.Entry(ventana_agregar, font=("Segoe UI", 11), width=22)
        entry_img.grid(row=3, column=1, padx=10, pady=10)

        def buscar_imagen():
            import subprocess
            from gestor.downloader import descargar_pngs
            nombre = entry_nombre.get()
            if not nombre:
                messagebox.showwarning("Nombre vacío", "Primero ingresa el nombre del artículo")
                return
            descargar_pngs(nombre, nombre)
            messagebox.showinfo("Imagen", f"Imagen descargada para '{nombre}' en static/assets/icons/")

        def seleccionar_imagen():
            from tkinter import filedialog
            ruta = filedialog.askopenfilename(title="Selecciona imagen", filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])
            if ruta:
                import shutil
                import os

                nombre = entry_nombre.get()
                if not nombre:
                    messagebox.showwarning("Nombre vacío", "Primero ingresa el nombre del artículo")
                    return
                httpnombre = httppath(nombre)
                destino = os.path.join("static/assets/icons", httpnombre + ".png")
                shutil.copy(ruta, destino)
                entry_img.delete(0, tk.END)
                entry_img.insert(0, destino)
                messagebox.showinfo("Imagen", f"Imagen copiada a {destino}")

        btn_buscar = ttk.Button(ventana_agregar, text="Buscar en web", command=buscar_imagen)
        btn_buscar.grid(row=4, column=0, padx=10, pady=5)
        btn_seleccionar = ttk.Button(ventana_agregar, text="Seleccionar local", command=seleccionar_imagen)
        btn_seleccionar.grid(row=4, column=1, padx=10, pady=5)

        def agregar_y_cerrar():
            from .articulos import agregar_articulo
            img_path = entry_img.get().strip()
            nombre = entry_nombre.get().strip()
            if not img_path:
                # Si no hay ruta, buscar imagen automáticamente
                from gestor.downloader import descargar_pngs
                descargar_pngs(nombre, nombre)
                img_path = f"static/assets/icons/{nombre}.png"
            # Se puede guardar la ruta de la imagen en la base de datos si se desea
            agregar_articulo(entry_nombre, combo_tipo, entry_cantidad, tree_articulos)
            ventana_agregar.destroy()

        btn_guardar = ttk.Button(ventana_agregar, text="Agregar", command=agregar_y_cerrar)
        btn_guardar.grid(row=5, column=0, columnspan=2, pady=18)

    btn_frame = tk.Frame(frame_articulos, bg="#f4f6fa")
    btn_frame.pack(pady=5)
    btn_agregar = ttk.Button(btn_frame, text="Agregar artículo", command=abrir_ventana_agregar)
    btn_agregar.pack(side="left", padx=8)
    btn_editar = ttk.Button(btn_frame, text="Editar", command=lambda: editar_articulo(tree_articulos, root))
    btn_editar.pack(side="left", padx=8)
    btn_eliminar = ttk.Button(btn_frame, text="Eliminar", command=lambda: eliminar_articulo(tree_articulos))
    btn_eliminar.pack(side="left", padx=8)

    cargar_articulos(tree_articulos)

    # TAB PRÉSTAMOS
    frame_prestamos = ttk.Frame(tabs)
    tabs.add(frame_prestamos, text="Préstamos")

    lbl_titulo_p = tk.Label(frame_prestamos, text="Gestión de Préstamos", font=("Segoe UI", 16, "bold"), bg="#f4f6fa", fg="#007bff")
    lbl_titulo_p.pack(pady=(10,0))

    form_prestamo = tk.Frame(frame_prestamos, bg="#f4f6fa")
    form_prestamo.pack(pady=10)

    tk.Label(form_prestamo, text="DNI de la persona:", font=("Segoe UI", 11), bg="#f4f6fa").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_persona_id = tk.Entry(form_prestamo, font=("Segoe UI", 11), width=22)
    entry_persona_id.grid(row=0, column=1, padx=10, pady=10)

    btn_prestar = ttk.Button(form_prestamo, text="Registrar Préstamo", command=lambda: registrar_prestamo(entry_persona_id, tree_prestamos))
    btn_prestar.grid(row=0, column=2, padx=10)
    btn_devolver = ttk.Button(form_prestamo, text="Registrar Devolución", command=lambda: devolver_prestamo(tree_prestamos))
    btn_devolver.grid(row=0, column=3, padx=10)

    tree_prestamos = ttk.Treeview(frame_prestamos, columns=("ID", "DNI", "Nombre", "Fecha", "Vigente"), show="headings")
    for col in ("ID", "DNI", "Nombre", "Fecha", "Vigente"):
        tree_prestamos.heading(col, text=col)
    tree_prestamos.pack(expand=True, fill="both", padx=20, pady=20)

    tree_prestamos.bind("<Double-1>", lambda event: ver_detalle_prestamo(event, tree_prestamos, root))

    cargar_prestamos(tree_prestamos)

    root.mainloop()
