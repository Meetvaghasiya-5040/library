setInterval(function() {
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        fetch(window.location.href)
            .then(res => res.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, "text/html");
                const newTable = doc.querySelector('table');
                if (newTable) {
                    table.innerHTML = newTable.innerHTML;
                }
            });
    });
}, 5000);