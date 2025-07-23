/**
 * Script principal para la interactividad del feed de noticias.
 *
 * Se encarga de:
 * 1. Marcar visualmente las noticias que el usuario ya ha visitado.
 * 2. Manejar la funcionalidad de expandir/colapsar el contenido completo.
 * 3. Gestionar la imagen de fallback en caso de errores de carga.
 */
document.addEventListener("DOMContentLoaded", () => {
    // Lógica para marcar noticias como leídas.
    const visitedIds = new Set(JSON.parse(localStorage.getItem("visitedIds") || "[]"));

    document.querySelectorAll(".news-item").forEach(item => {
        // Encontramos el enlace dentro del h2.
        const titleLink = item.querySelector(".news-title a");
        // Encontramos el botón de expansión dentro de <details>.
        const expandButton = item.querySelector("details summary");
        // Obtenemos el ID de la noticia desde el contenedor principal.
        const newsId = item.dataset.id;

        // Si la noticia ya está en nuestro 'Set', le agregamos la clase CSS 'visited'.
        if (visitedIds.has(newsId)) {
            item.classList.add("visited");
        }

        // Lógica de marcado como leído al hacer clic en el título.
        if (titleLink) {
            titleLink.addEventListener("click", () => {
                if (!visitedIds.has(newsId)) {
                    visitedIds.add(newsId);
                    localStorage.setItem("visitedIds", JSON.stringify([...visitedIds]));
                    item.classList.add("visited");
                }
            });
        }

        // Lógica de expansión/colapsado del contenido completo.
        if (expandButton) {
            expandButton.addEventListener("click", (event) => {
                event.preventDefault(); // Evita que se navegue al hacer clic en "Leer más".
                const contentDetails = expandButton.closest('details');
                contentDetails.open = !contentDetails.open;
            });
        }

        // Lógica para la imagen de fallback.
        const thumbnail = item.querySelector(".thumbnail");
        if (thumbnail) {
            thumbnail.onerror = () => {
                thumbnail.src = 'assets/img/fallback.jpg';
            };
        }
    });
});