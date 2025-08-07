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


app = flask.Flask(__name__)

@app.route("/")
def index(): 
    return flask.render_template("index.html")

@app.route("/api")
def api_index():
    search = flask.request.args.get("search")
    try:
        connection = startConnection()
    except Exception:
        connection = False
    if connection:
        cursor = connection.cursor()
        if search:  
            cursor.execute("SELECT * FROM items WHERE nombre ILIKE %s", (f"%{search}%",))
        else:
            cursor.execute("SELECT * FROM items")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        connection.close()

        # handshake: transformar a lista de dicts

        stocks = [row_to_dict(row) for row in rows]
        return flask.jsonify(stocks)
    else: 
        
        stocks = [
            {
                "id": 1,
                "nombre": "destornillador punta plana 8",
                "descripcion": "destornillador de punta plana de metrica 8",
                "tamano": 8,

                "cantidad_total": float(2),
                "cantidad_disponible": float(1),
                "categoria_id": 0,
                "ubicacion_id": 0,
                "tipo_item": 0
            },{
                "id": 1,
                "nombre": "cable de aluminio",
                "descripcion": "cable de aluminio con aislamiento. soporta hasta 3 amperes a 300 volts",
                "tamano": 20,
                "cantidad_total": float(2),
                "cantidad_disponible": float(1),
                "categoria_id": 0,
                "ubicacion_id": 0,
                "tipo_item": 0
            },{
                "id": 1,
                "nombre": "llave francesa",
                "tamano": 10,
                "descripcion": "llave francesa grande",
                "cantidad_total": float(2),
                "cantidad_disponible": float(1),
                "categoria_id": 0,
                "ubicacion_id": 0,
                "tipo_item": 0
            }
        ]
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



app.run(port=8000, debug=True)