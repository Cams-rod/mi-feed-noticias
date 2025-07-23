/**
 * Script principal para la interactividad del feed de noticias.
 *
 * Se encarga de:
 * 1. Marcar visualmente las noticias que el usuario ya ha visitado.
 * 2. Manejar la funcionalidad de expandir/colapsar el contenido completo.
 * 3. Gestionar la imagen de fallback en caso de errores de carga.
 */
document.addEventListener("DOMContentLoaded", () => {
    // 1. Lógica para marcar noticias como leídas.
    // Usamos un 'Set' para guardar los IDs de las noticias visitadas y evitar duplicados.
    const visitedIds = new Set(JSON.parse(localStorage.getItem("visitedIds") || "[]"));

    // Seleccionamos cada tarjeta de noticia para aplicar la lógica.
    document.querySelectorAll(".news-item").forEach(item => {
        const titleLink = item.querySelector(".news-title");
        const contentDetails = item.querySelector("details");
        const image = item.querySelector(".thumbnail");
        
        // Obtenemos el ID único de la noticia desde el atributo de datos.
        const newsId = titleLink.dataset.id;

        // Si la noticia ya está en nuestro 'Set', le agregamos la clase CSS 'visited'.
        if (visitedIds.has(newsId)) {
            item.classList.add("visited");
        }

        // 2. Lógica para expandir/colapsar contenido y marcar como leído.
        // Al hacer clic en el título de la noticia:
        titleLink.addEventListener("click", (event) => {
            // Prevenimos que el navegador navegue a la URL por defecto del enlace.
            event.preventDefault(); 
            
            // Si existe el elemento <details>, cambiamos su estado de abierto/cerrado.
            if (contentDetails) {
                contentDetails.open = !contentDetails.open;
            }

            // Agregamos el ID al 'Set' si no estaba.
            if (!visitedIds.has(newsId)) {
                visitedIds.add(newsId);
                // Guardamos el Set actualizado en el almacenamiento local.
                localStorage.setItem("visitedIds", JSON.stringify([...visitedIds]));
                // Le agregamos la clase 'visited' a la tarjeta de la noticia.
                item.classList.add("visited");
            }
        });

        // 3. Lógica para la imagen de fallback.
        // Si la imagen tiene un error al cargar, usamos la imagen de fallback.
        if (image) {
            image.onerror = () => {
                image.src = 'assets/img/fallback.jpg';
                // Opcional: Podrías añadir una clase para cambiar el estilo si usas una imagen de fallback.
                image.classList.add('fallback-image');
            };
        }
    });
});
