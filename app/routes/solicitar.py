from flask import Blueprint, render_template, request, jsonify
from ..db import start_connection

import secrets
import datetime
import bcrypt

bp = Blueprint('solicitar', __name__)

@bp.route("/api/solicitar/", methods=["POST"])
def validation():
    data = request.json
    token = data.get("token")
    if not token:
        return jsonify({"error": "Token is required"}), 400
    connection = start_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM sessions WHERE session_token = ?", (token,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"error": "Invalid token"}), 401
    solicitudes = data.get("solicitudes", [])
    if not solicitudes: 
        return jsonify({"error": "No solicitudes provided"}), 400  
    cursor.execute("INSERT INTO prestamos (persona_id, fecha_prestamo, fecha_devolucion) VALUES (?, ?, ?)", (user[0], datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=3)))
    prestamo_id = cursor.lastrowid
    for solicitud in solicitudes:
        cursor.execute("INSERT INTO detalle_prestamo_item (prestamo_id, item_id, cantidad) VALUES (?, ?, ?)", (prestamo_id, solicitud['id'], solicitud['cantidad']))
    connection.commit()
    cursor.close()
    return jsonify({"message": "Solicitud realizada con éxito"}), 200        
