import flask 
import os
import dotenv
import sqlite3

dotenv.load_dotenv()

def startConnection():
    return sqlite3.connect("db")

def row_to_dict(row):
    return {
        "id": row[0],
        "nombre": row[1],
        "descripcion": row[2],
        "cantidad_total": float(row[3]),
        "cantidad_disponible": float(row[4]),
        "categoria_id": row[5],
        "ubicacion_id": row[6],
        "tipo_item": row[7],
        "tamano": row[8]
    }

app = flask.Flask(__name__)

@app.route("/")
def index(): 
    return flask.render_template("index.html")

@app.route("/api")
def api_index():
    search = flask.request.args.get("search")
    connection = startConnection()
    connection.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
    cursor = connection.cursor()

    if search:  
        # Usar LIKE (SQLite no tiene ILIKE); convertir a minúsculas
        cursor.execute(
            "SELECT * FROM items WHERE LOWER(nombre) LIKE ?",
            (f"%{search.lower()}%",)
        )
    else:
        cursor.execute("SELECT * FROM items")

    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    # Transformar a lista de dicts
    stocks = [row_to_dict(row) for row in rows]
    return flask.jsonify(stocks)

@app.route("/api/pedidos")
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
    return flask.jsonify(response)

@app.route("/pedidos/")
def pedidos(): 
    return flask.render_template("pedidos.html")

@app.route("/register/")
def register():
    return flask.render_template("registro.html")

@app.route("/login/")
def login():
    return flask.render_template("login.html")

if __name__ == "__main__":
    app.run(port=8000, debug=True)
