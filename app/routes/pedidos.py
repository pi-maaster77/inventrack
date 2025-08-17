from flask import Blueprint, render_template, jsonify

bp = Blueprint('pedidos', __name__)

@bp.route("/pedidos/")
def pedidos():
    return render_template("pedidos.html")

@bp.route("/api/pedidos")
def api_pedidos():
    response = [{
        "nombre": "llave francesa",
        "tamano": "10",
        "cantidad": "1",
        "ubicacion": "estante 2",
        "hora": "13:30",
        "devolucion": "16:45",
        "id": 14
    }]
    return jsonify(response)
