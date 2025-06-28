import flask 

app = flask.Flask(__name__)

@app.route("/")
def index(): 
    return flask.render_template("index.html")

@app.route("/api")
def api_index():
    search = flask.request.args.get("search")
    print(search)
    response = [{
        "imagen": "destornillador.png",
        "nombre": "destornillador",
        "tamano": "1/2",
        "cantidad": "170",
        "ubicacion": "estante 2"
    }]
    return flask.jsonify(response)

@app.route("/api/pedidos")
def api_pedidos():
    response = [{
        "nombre": "llave",
        "tamano": "8",
        "cantidad": "5",
        "ubicacion": "estante 2",
        "hora": "-1:61",
        "devolucion": "25:99",
        "id": 14
    }]
    return flask.jsonify(response)

@app.route("/pedidos/")
def pedidos(): 
    return flask.render_template("pedidos.html")



app.run(port=8000, debug=True)