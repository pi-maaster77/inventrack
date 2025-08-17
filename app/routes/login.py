from flask import Blueprint, render_template, request, jsonify

bp = Blueprint('login', __name__)

@bp.route("/login/")
def register():
    return render_template("login.html")

@bp.route("/api/login", methods=["POST"])
def api_registro():
    data = request.form
    print(data)
    return jsonify({"message": "Registro exitoso"}), 201
