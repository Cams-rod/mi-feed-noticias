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
    const visitedIds = new Set(JSON.parse(localStorage.getItem("visitedIds") || "[]"));

    document.querySelectorAll(".news-item").forEach(item => {
        const titleLink = item.querySelector(".news-title");
        const contentDetails = item.querySelector("details");
        const image = item.querySelector(".thumbnail");
        
        const newsId = titleLink.dataset.id;

        if (visitedIds.has(newsId)) {
            item.classList.add("visited");
        }

        // --- CAMBIO IMPORTANTE: Lógica de Marcar como Leído ---
        // Al hacer clic en el título, solo se marca como leído.
        // NO PREVENIMOS el comportamiento por defecto, para que el enlace funcione.
        titleLink.addEventListener("click", () => {
            if (!visitedIds.has(newsId)) {
                visitedIds.add(newsId);
                localStorage.setItem("visitedIds", JSON.stringify([...visitedIds]));
                item.classList.add("visited");
            }
        });
        
        // --- NUEVA LÓGICA: Separamos la expansión del contenido ---
        // Si existe el elemento <details> (es decir, hay contenido completo)...
        if (contentDetails) {
            // ...añadimos un listener al botón de expansión (<summary>) dentro de <details>.
            // Esto evita que el clic en el título abra/cierre el contenido.
            contentDetails.querySelector('summary').addEventListener("click", (event) => {
                // Aquí sí usamos preventDefault() para evitar la navegación.
                event.preventDefault();
                contentDetails.open = !contentDetails.open;
            });
        }

        // 3. Lógica para la imagen de fallback.
        if (image) {
            image.onerror = () => {
                image.src = 'assets/img/fallback.jpg';
                image.classList.add('fallback-image');
            };
        }
    });
});