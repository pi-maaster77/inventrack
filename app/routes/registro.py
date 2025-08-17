from flask import Blueprint, render_template, request, jsonify

bp = Blueprint('registro', __name__)

@bp.route("/register/")
def register():
    return render_template("registro.html")

@bp.route("/api/registro", methods=["POST"])
def api_registro():
    data = request.form
    print(data)
    return jsonify({"message": "Registro exitoso"}), 201
