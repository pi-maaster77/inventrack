import sqlite3

def start_connection():
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
