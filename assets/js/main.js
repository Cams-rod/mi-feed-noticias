document.addEventListener("DOMContentLoaded", () => {
    // Almacenar los IDs de las noticias visitadas en localStorage
    const visitedIds = new Set(JSON.parse(localStorage.getItem("visitedIds") || "[]"));

    // Marcar visualmente los elementos que ya fueron visitados
    document.querySelectorAll(".news-title").forEach(title => {
        const id = title.dataset.id;
        const item = title.closest(".news-item");

        if (visitedIds.has(id)) {
            item.classList.add("visited");
        }

        title.addEventListener("click", () => {
            // Guardar el ID en el set y localStorage
            visitedIds.add(id);
            localStorage.setItem("visitedIds", JSON.stringify([...visitedIds]));
            
            // Añadir la clase para el estilo
            item.classList.add("visited");
        });
    });
});