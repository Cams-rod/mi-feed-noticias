# Mi Portal de Noticias Estático

Este proyecto es un generador de sitios estáticos, inspirado en la filosofía del Jamstack, que transforma múltiples feeds RSS en un portal de noticias moderno y automatizado. Con un diseño minimalista y cálido al estilo Studio Ghibli, el sitio se actualiza de forma automática y se despliega sin necesidad de un servidor activo.

## Características

* **Generador Estático:** Utiliza un script de Python para leer, procesar y consolidar las noticias en un archivo index.html. El sitio resultante es puramente estático, lo que garantiza una carga ultrarrápida y una seguridad inherente.
* **Diseño Ghibli:** Un diseño visual minimalista, con una paleta de colores suaves y tipografía cálida, que crea una experiencia de lectura relajante y única.
* **Personalización del Usuario:** Utiliza JavaScript y localStorage para marcar y recordar las noticias que ya has visitado, mejorando la experiencia de lectura de cada usuario.
* **Automatización:** Gracias a GitHub Actions, el portal se actualiza automáticamente cada 24 horas, asegurando que el contenido esté siempre fresco y al día, sin intervención manual.
* **Seguridad:** El contenido de cada feed RSS es sanitizado con la biblioteca bleach para prevenir ataques de Cross-Site Scripting (XSS).
* **Mantenimiento:** La gestión de las fuentes de noticias es tan fácil como editar un simple archivo feeds.txt.

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
