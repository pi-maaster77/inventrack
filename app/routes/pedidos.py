from flask import Blueprint, render_template, jsonify, request
from ..db import start_connection

bp = Blueprint('pedidos', __name__)

@bp.route("/pedidos/")
def pedidos():
    return render_template("pedidos.html")

@bp.route("/api/pedidos", methods=["GET"])
def api_pedidos():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token no proporcionado"}), 401

    db = start_connection()
    cursor = db.cursor()
    cursor.execute("""
        SELECT p.id, p.fecha_prestamo, p.fecha_devolucion, i.nombre, dpi.cantidad
        FROM sessions s
        JOIN prestamos p ON p.persona_id = s.user_id
        JOIN detalle_prestamo_item dpi ON dpi.prestamo_id = p.id
        JOIN items i ON i.id = dpi.item_id
        WHERE s.session_token = ?
        ORDER BY p.fecha_prestamo DESC
    """, (token,))
    rows = cursor.fetchall()
    cursor.close()
    print(rows)
    prestamos = {}
    for row in rows:
        prestamo_id = row[0]
        if prestamo_id not in prestamos:
            prestamos[prestamo_id] = {
                "fecha": row[1],
                "devolucion": row[2],
                "items": []
            }
        prestamos[prestamo_id]["items"].append({
            "nombre": row[3],
            "cantidad": row[4]
        })

    # Convertir a lista
    lista_prestamos = []
    for id, data in prestamos.items():
        lista_prestamos.append({
            "fecha": data["fecha"],
            "devolucion": data["devolucion"] or "Sin devolver",
            "items": data["items"]
        })

    return jsonify(lista_prestamos), 200
