document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('.topbar .left a, .sidebar a');
    const contentDiv = document.getElementById('content');

    function setActive(page) {
        links.forEach(l => {
            if (l.getAttribute('data-page') === page) {
                l.classList.add('active');
            } else {
                l.classList.remove('active');
            }
        });
    }

    function loadPage(url) {
        fetch(url, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => {
            if (!response.ok) throw new Error("Error al cargar la página");
            return response.text();
        })
        .then(html => {
            contentDiv.innerHTML = html;
        })
        .catch(error => {
            console.error('Error:', error);
            contentDiv.innerHTML = "<p>Error al cargar contenido.</p>";
        });
    }

    // Evento al hacer clic
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const page = this.getAttribute('data-page');
            setActive(page);
            loadPage(page);
        });
    });

    // 🚀 CARGAR AUTOMÁTICAMENTE "VENTAS" AL INICIO
    const defaultPage = links[0].getAttribute('data-page'); // la primera (ventas)
    setActive(defaultPage);
    loadPage(defaultPage);
});
