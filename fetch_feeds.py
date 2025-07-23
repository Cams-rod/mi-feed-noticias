"""
Motor de generación de feed RSS.

Este script lee URLs de feeds RSS, extrae los datos más recientes,
los sanitiza, y genera un archivo JSON y una página HTML estática.
El contenido se guarda en la carpeta 'dist/' para su publicación.
                       by Chams-Rod
"""
import feedparser
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import hashlib
import os
from jinja2 import Environment, FileSystemLoader
import bleach
import shutil
import logging


# Configuración del logging para mejor depuración en GitHub Actions
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Headers para simular un navegador y evitar bloqueos
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36'}

# Etiquetas y atributos permitidos para la sanitización de HTML
# Esto previene ataques de Cross-Site Scripting (XSS)
ALLOWED_TAGS = [
    'p', 'b', 'i', 'em', 'strong', 'a', 'ul', 'ol', 'li', 'br', 'img',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'pre', 'code',
    'span', 'div'
]
# Permite atributos de clase y estilo en cualquier etiqueta
ALLOWED_ATTRS = {
    '*': ['class', 'style'], 
    'a': ['href', 'title'],
    'img': ['src', 'alt', 'width', 'height'],
}

# --- Funciones de Lógica ---
def extract_image(url):
    """
    Intenta extraer la URL de una imagen destacada de una página web.
    
    Args:
        url (str): La URL de la página web.

    Returns:
        str: La URL de la imagen encontrada o None si no se encuentra.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Intentar extraer de la meta tag
        image = soup.find("meta", property="og:image")
        if image and image.get("content"):
            return image["content"]
        
        # Intentar extraer del icono del sitio
        icon = soup.find("link", rel="icon")
        if icon and icon.get("href"):
            return icon["href"]
            
    except Exception as e:
        logging.warning(f"⚠️ Error extrayendo imagen de {url}: {e}")
    return None

def extract_content(entry):
    """
    Extrae el contenido de una entrada del feed de forma segura,
    priorizando el contenido completo.

    Args:
        entry (dict): La entrada del feed (puede ser un FeedParserDict o un dict simple).

    Returns:
        str: El contenido HTML de la entrada.
    """
    # Usamos .get() para evitar errores si el campo no existe.
    content_value = entry.get('content')
    summary_value = entry.get('summary')
    
    # Verificamos si hay contenido completo y si es diferente del resumen
    has_full_content = False
    if content_value and isinstance(content_value, list) and content_value[0].get('value'):
        full_content_text = content_value[0].get('value')
        if full_content_text != summary_value:
            has_full_content = True
        return full_content_text, has_full_content
    
    # Si no hay contenido completo, usamos el resumen
    return summary_value or "No hay contenido disponible.", has_full_content

def extract_summary_text(html):
    """
    Crea un resumen de texto plano a partir de contenido HTML.
    
    Args:
        html (str): El contenido HTML.
        max_length (int): La longitud máxima del resumen.

    Returns:
        str: El resumen de texto.
    """
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text().strip()
    return text[:300] + "..." if len(text) > 300 else text

def generate_id(link):
    """
    Genera un ID único y determinista para una entrada usando su URL.
    
    Args:
        link (str): La URL de la entrada.

    Returns:
        str: El hash MD5 de la URL.
    """
    return hashlib.md5(link.encode('utf-8')).hexdigest()

def process_feeds():
    """
    Lee las URLs de los feeds, procesa las entradas y devuelve una lista unificada.
    
    Returns:
        list: Una lista de diccionarios, cada uno representando una noticia.
    """
    all_entries = []

    try:
        with open("feeds.txt", "r") as file:
            urls = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        logging.error("❌ feeds.txt no encontrado.")
        return []

    for url in urls:
        logging.info(f"📡 Leyendo feed: {url}")
        try:
            feed = feedparser.parse(url, request_headers=HEADERS)
            
            if feed.bozo:
                logging.warning(f"⚠️ Error al parsear feed {url}: {feed.bozo_exception}")
                continue
            
            for entry in feed.entries[:5]: 
                # --- CORRECCIÓN AQUÍ: Llamamos a la función solo una vez ---
                full_content, has_full_content = extract_content(entry)
                
                # Sanitizar el contenido para prevenir XSS
                sanitized_content = bleach.clean(
                    full_content,
                    tags=ALLOWED_TAGS,
                    attributes=ALLOWED_ATTRS,
                    strip=True
                )
                
                # Extraemos el resumen del contenido sanitizado
                summary_text = extract_summary_text(sanitized_content)

                image_url = extract_image(entry.link)
                image = image_url if image_url and image_url.strip() else 'assets/img/fallback.jpg'
                date = entry.get("published_parsed") or entry.get("updated_parsed")
                iso_date = datetime(*date[:6]).isoformat() if date else None

                all_entries.append({
                    "id": generate_id(entry.link),
                    "title": entry.title,
                    "link": entry.link,
                    "image": image,
                    "summary": summary_text,
                    "content": sanitized_content,
                    "published": iso_date,
                    "has_full_content": has_full_content
                })
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Error de red al acceder a {url}: {e}")
        except Exception as e:
            logging.error(f"❌ Error inesperado al procesar {url}: {e}")

    all_entries.sort(key=lambda x: x["published"] or "", reverse=True)
    return all_entries

def main():
    """
    Función principal para unir todo el proceso completo de generación.
    """
    # Crear carpeta de salida si no existe
    os.makedirs("dist", exist_ok=True)
    os.makedirs("dist/assets/css", exist_ok=True)
    os.makedirs("dist/assets/js", exist_ok=True)
    os.makedirs("dist/assets/img", exist_ok=True)
    
    news_entries = process_feeds()
    
    # 1. Guardar como JSON
    with open("dist/news.json", "w", encoding="utf-8") as f:
        json.dump(news_entries, f, ensure_ascii=False, indent=2)
    logging.info("✅ news.json generado.")

    # 2. Renderizar index.html desde plantilla
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("index.html")

    rendered_html = template.render(news=news_entries)

    with open("dist/index.html", "w", encoding="utf-8") as f:
        f.write(rendered_html)
    logging.info("✅ index.html generado en la carpeta dist/")

# Copiar archivos estáticos (CSS y JS) a la carpeta dist
    logging.info("➡️ Copiando assets (CSS y JS)...")

    # Copia tu CSS
    shutil.copytree("assets/css", "dist/assets/css", dirs_exist_ok=True)
    
    # Copia tu JS
    shutil.copytree("assets/js", "dist/assets/js", dirs_exist_ok=True)

    shutil.copytree("assets/img", "dist/assets/img", dirs_exist_ok=True)
    
    logging.info("✅ Assets copiados a dist/")
if __name__ == "__main__":
    main()