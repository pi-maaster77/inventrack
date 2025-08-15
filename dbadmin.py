import sqlite3

def execute_sql_file(db_file, sql_file):
    # Conectar a la base de datos SQLite (si no existe, se crea)
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    
    # Leer el contenido del archivo .sql
    with open(sql_file, 'r') as file:
        sql_script = file.read()
    
    # Ejecutar todas las instrucciones SQL del archivo
    try:
        cursor.executescript(sql_script)
        connection.commit()
        
        print(f"Archivo {sql_file} ejecutado correctamente en la base de datos {db_file}")
    except sqlite3.Error as e:
        print(f"Error al ejecutar el archivo SQL: {e}")
    finally:
        print(cursor.fetchall())
        # Cerrar la conexión
        connection.close()

if __name__ == "__main__":
    # Rutas a los archivos
    db_file = "db"  # Archivo de la base de datos SQLite
    sql_file = "request.sql"  # Archivo SQL con las instrucciones
    
    # Ejecutar el archivo SQL en la base de datos SQLite
    execute_sql_file(db_file, sql_file)
