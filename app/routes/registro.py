from flask import Blueprint, render_template, request, jsonify
import bcrypt
from ..db import start_connection

import secrets
import datetime

bp = Blueprint('registro', __name__)

@bp.route("/register/")
def register():
    return render_template("registro.html")

@bp.route("/api/registro", methods=["POST"])
def api_registro():
    data = request.form
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    dni = data.get("dni")
    password = data.get("password")
    if not nombre or not apellido or not dni or not password:
        return jsonify({"error": "Faltan datos"}), 400
    db = start_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM personas WHERE dni = ?", (dni,))
    user = cursor.fetchone()
    if user:
        return jsonify({"error": "El usuario ya existe"}), 400
    cursor.execute("INSERT INTO personas (nombre, apellido, dni, passwd, tipo_persona) VALUES (?, ?, ?, ?, ?)", 
                   (nombre, apellido, dni, bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), "Alumno"))
    db.commit()
    token = secrets.token_urlsafe(32)
    creation_time = datetime.datetime.now()
    expiration_time = creation_time + datetime.timedelta(days=30)
    cursor.execute(
        "INSERT INTO sessions (user_id, session_token, created_at, expires_at) VALUES (?, ?, ?, ?)",
        (dni, token, creation_time, expiration_time)
    )
    db.commit()
    cursor.close()

    return jsonify({"message": "Registro exitoso", "token": token}), 201
