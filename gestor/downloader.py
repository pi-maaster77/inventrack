import os
import requests
from bs4 import BeautifulSoup
from .httppath import httppath
import urllib.parse
import unicodedata
import re

def descargar_pngs(busqueda, nombre):
    busqueda = busqueda.replace(' ', '-').lower()
    url = f'https://www.stickpng.com/es/search?q={busqueda}'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    imagenes = soup.find_all('img')

    for img in imagenes:
        src = img.get('src')
        if src and src.endswith('.png'):
            img_url = src if src.startswith('http') else 'https:' + src
            http_path = httppath(nombre)
            img_name = os.path.join('static/assets/icons', os.path.basename(http_path) + '.png')
            try:
                img_data = requests.get(img_url).content

                # Ruta compatible HTTP (relativa y con /)
                
                print(f'Descargada: {img_name}')
                with open(img_name, 'wb') as f:
                    f.write(img_data)
                break
            except Exception as e:
                print(f'Error al descargar {img_name}: {e}')

if __name__ == "__main__":
    descargar_pngs('destornillador', "prueba_destornillador")
