import flask 
import psycopg2
import os
import dotenv


dotenv.load_dotenv()

def startConnection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


app = flask.Flask(__name__)

@app.route("/")
def index(): 
    return flask.render_template("index.html")

@app.route("/api")
def api_index():
    search = flask.request.args.get("search")
    connection = startConnection()
    cursor = connection.cursor()
    if search:  
        cursor.execute("SELECT * FROM items WHERE nombre LIKE %s", (f"%{search}%",))
    else:
        cursor.execute("SELECT * FROM items")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    connection.close()

    # handshake: transformar a lista de dicts
    def row_to_dict(row):
        return {
            "id": row[0],
            "nombre": row[1],
            "descripcion": row[2],
            "cantidad_total": float(row[3]),
            "cantidad_disponible": float(row[4]),
            "categoria_id": row[5],
            "ubicacion_id": row[6],
            "tipo_item": row[7]
        }

    stocks = [row_to_dict(row) for row in rows]
    return flask.jsonify(stocks)

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