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
    toolID = data.get("id")
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

    cursor.execute("", (session[0],))
