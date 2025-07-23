# Mi Portal de Noticias Estático

Este proyecto es un generador de sitios estáticos para feeds de noticias RSS, inspirado en el estilo de Studio Ghibli. Utiliza Python para leer múltiples fuentes RSS, consolida las noticias y genera un sitio web estático y personalizable que se despliega automáticamente en GitHub Pages.

## Características

* **Generador Estático:** El sitio se genera completamente en el servidor (en GitHub Actions), eliminando la necesidad de un backend en vivo.
* **Diseño Ghibli:** Estilo visual minimalista y cálido.
* **Personalización del Usuario:** Utiliza `localStorage` para recordar las noticias que ya has leído.
* **Automatización:** Un "cronjob" en GitHub Actions actualiza el sitio cada 24 horas.
* **Seguridad:** El contenido de los feeds se sanitiza con `bleach` para prevenir ataques XSS.

## Estructura del Proyecto
├── .github/                      # Configuración de GitHub Actions
├── assets/                       # Archivos estáticos del frontend (CSS, JS, Imágenes)
├── dist/                         # Carpeta de salida con el sitio web generado
├── templates/                    # Plantilla HTML de Jinja2
├── feeds.txt                     # Fuentes RSS a leer (una por línea)
├── fetch_feeds.py                # Script principal del generador
├── test_fetch_feeds.py           # Pruebas unitarias para el script
├── requirements.txt              # Dependencias de Python
├── LICENSE                       # Licencia del proyecto (MIT)
└── README.md                     # Este archivo

## Guía de Uso Local

Para probar el generador en tu máquina antes de subirlo:

1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/mi-feed-noticias.git](https://github.com/tu-usuario/mi-feed-noticias.git)
    cd mi-feed-noticias
    ```
2.  **Crea un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa venv\Scripts\activate
    ```
3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Ejecuta el script de generación:**
    ```bash
    python fetch_feeds.py
    ```
    El sitio web estático se generará en la carpeta `dist/`.

5.  **Abre el sitio:**
    Abre el archivo `dist/index.html` en tu navegador web.

## Pruebas Unitarias

Para ejecutar las pruebas y asegurar que la lógica principal funciona correctamente:

```bash
python -m unittest
