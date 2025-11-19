// Helper to ensure AJAX/fetch requests include CSRF token for same-origin requests
(function(){
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    let csrftoken = getCookie('csrftoken');
    // Si la cookie no existe (p. ej. HTML inyectado sin cookie), intentar obtener
    // el token desde un input hidden generado por {% csrf_token %}
    if (!csrftoken) {
        const el = document.querySelector('input[name="csrfmiddlewaretoken"]');
        if (el) {
            csrftoken = el.value;
        }
    }

    function sameOrigin(url) {
        // url could be relative or absolute
        const host = window.location.host; // includes port
        const protocol = window.location.protocol;
        const sr_origin = protocol + '//' + host;
        return (url === sr_origin || url.startsWith(sr_origin + '/')) || !(/^(https?:)?\/\//i.test(url));
    }

    // Wrap fetch to add X-CSRFToken header for same-origin non-GET requests
    if (window.fetch) {
        const _fetch = window.fetch.bind(window);
        window.fetch = function(input, init) {
            try {
                let url = (typeof input === 'string') ? input : input.url;
                init = init || {};
                // Asegurar que fetch envíe cookies para same-origin si no se especificó
                if (!('credentials' in init)) {
                    init.credentials = 'same-origin';
                }
                const method = (init.method || (typeof input === 'object' && input.method) || 'GET').toUpperCase();
                if (sameOrigin(url) && !['GET','HEAD','OPTIONS','TRACE'].includes(method)) {
                    init.headers = new Headers(init.headers || {});
                    if (!init.headers.has('X-CSRFToken')) {
                        init.headers.set('X-CSRFToken', csrftoken);
                    }
                }
            } catch (e) {
                // silently ignore
            }
            return _fetch(input, init);
        };
    }

    // jQuery support: set header for AJAX
    if (window.jQuery) {
        window.jQuery.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && sameOrigin(settings.url)) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        });
    }
})();
