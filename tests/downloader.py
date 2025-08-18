import os
import requests
from bs4 import BeautifulSoup

def descargar_pngs(busqueda):
    busqueda = busqueda.replace(' ', '-').lower()
    url = f'https://www.stickpng.com/es/search?q={busqueda}'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    os.makedirs('imagenes_png', exist_ok=True)

    imagenes = soup.find_all('img')

    for img in imagenes:
        src = img.get('src')
        if src and src.endswith('.png'):
            img_url = src if src.startswith('http') else 'https:' + src
            img_name = os.path.join('imagenes_png', os.path.basename(src))
            try:
                img_data = requests.get(img_url).content
                with open(img_name, 'wb') as f:
                    f.write(img_data)
                print(f'Descargada: {img_name}')
            except Exception as e:
                print(f'Error al descargar {img_name}: {e}')

descargar_pngs('destornillador')
