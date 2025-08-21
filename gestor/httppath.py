import os
import urllib.parse
import unicodedata
import re

# esta funcion convierte un nombre de archivo a un nombre compatible con HTTP
def httppath(img_name):
    
    # 1. Convertir a minúsculas
    nombre = img_name.lower()
    
    # 2. Eliminar acentos y diacríticos
    nombre = unicodedata.normalize('NFKD', nombre).encode('ascii', 'ignore').decode('ascii')
    
    # 3. Reemplazar espacios y caracteres no válidos por guiones
    nombre = re.sub(r'[^a-z0-9_.-]', '-', nombre)
    
    # 4. Reemplazar múltiples guiones consecutivos por uno solo
    nombre = re.sub(r'-+', '-', nombre)
    
    # 5. Quitar guiones iniciales o finales
    nombre = nombre.strip('-')
    
    # 6. Escapar caracteres para URL
    nombre = urllib.parse.quote(nombre)
    
    return nombre

# Ejemplo de uso
print(httppath("Mi foto #1.jpg"))
# Salida: mi-foto-1.jpg
