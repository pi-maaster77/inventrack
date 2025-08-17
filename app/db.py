import sqlite3

def start_connection():
    print("Conectando a la base de datos...")
    return sqlite3.connect("db")

def row_to_dict(row):
    return {
        "id": row[0],
        "nombre": row[1],
        "descripcion": row[2],
        "cantidad_total": int(row[3]),
        "cantidad_disponible": int(row[4]),
        "ubicacion_id": row[5],
        "tipo_item": row[6],
    }
    