from flask import Blueprint, render_template, request, jsonify
from ..db import start_connection, row_to_dict

bp = Blueprint('main', __name__)

@bp.route("/")
def index(): 
    return render_template("index.html")

@bp.route("/api")
def api_index():
    search = request.args.get("search")
    conn = start_connection()
    conn.row_factory = lambda cursor, row: row_to_dict(row)
    cursor = conn.cursor()

    if search:
        cursor.execute(
            "SELECT id, nombre, descripcion, cantidad_total, cantidad_disponible, ubicacion_id, tipo_item FROM items WHERE LOWER(nombre) LIKE ?",
            (f"%{search.lower()}%",)
        )
    else:
        cursor.execute("SELECT id, nombre, descripcion, cantidad_total, cantidad_disponible, ubicacion_id, tipo_item FROM items")

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    stocks = rows
    return jsonify(stocks)
