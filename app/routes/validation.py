from flask import Blueprint, render_template, request, jsonify
from ..db import start_connection

import secrets
import datetime
import bcrypt

bp = Blueprint('validation', __name__)

@bp.route("/api/validate/", methods=["POST"])
def validation():
    data = request.json
    token = data.get("token")
    print(f"Validando token: {token}")

    if not token:
        return jsonify({"valid": False, "error": "Faltan datos"}), 400

    db = start_connection()
    cursor = db.cursor()

    cursor.execute("SELECT user_id, session_token, created_at, expires_at FROM sessions WHERE session_token = ?", (token,))
    session = cursor.fetchone()
    print(session)
    if not session:
        cursor.close()
        return jsonify({"valid": False, "error": "Token inválido"}), 401
    # Verificar si el token ha expirado. 2025-09-17 01:22:02.724883
    expiration = datetime.datetime.strptime(session[3], "%Y-%m-%d %H:%M:%S.%f")
    if expiration < datetime.datetime.now():
        cursor.execute("DELETE FROM sessions WHERE session_token = ?", (token,))
        db.commit()
        cursor.close()
        return jsonify({"valid": False, "error": "Token expirado"}), 401

    cursor.execute("SELECT nombre, apellido FROM personas WHERE dni = ?", (session[0],))
    user = cursor.fetchone()
    print(user)
    cursor.close()

    if not user:
        return jsonify({"valid": False, "error": "Usuario no encontrado"}), 404

    user_data = {
        "nombre": user[0],
        "apellido": user[1]
    }

    return jsonify({"valid": True, "message": "Token válido", "user": user_data}), 200
