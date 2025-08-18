from flask import Blueprint, render_template, request, jsonify
from ..db import start_connection

import secrets
import datetime
import bcrypt

bp = Blueprint('login', __name__)

@bp.route("/login/")
def login():
    return render_template("login.html")

@bp.route("/api/login/", methods=["POST"])
def api_login():
    data = request.form
    dni = data.get("username")
    password = data.get("password")
    if not dni or not password:
        return jsonify({"error": "Faltan datos"}), 400
    db = start_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM personas WHERE dni = ?", (dni,))
    user = cursor.fetchone()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user[4].encode('utf-8')):
        return jsonify({"error": "Credenciales inválidas"}), 401
    token = secrets.token_urlsafe(32)
    creation_time = datetime.datetime.now()
    expiration_time = creation_time + datetime.timedelta(days=30)  # Expira en
    cursor.execute(
        "INSERT OR REPLACE INTO sessions (user_id, session_token, created_at, expires_at) VALUES (?, ?, ?, ?)",
        (dni, token, creation_time, expiration_time)
    )
    db.commit()
    cursor.execute("SELECT * FROM sessions WHERE user_id = ?", (dni,))
    result = cursor.fetchone()
    cursor.close()
    if not result:
        return jsonify({"error": "Error al crear la sesión"}), 500
    print(user)
    return jsonify({"message": "Registro exitoso", "token": token}), 201
