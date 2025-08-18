async function renderizarStock() {
    const busqueda = document.getElementById("search-bar");
    const rawStock = await fetch(`/api?search=${busqueda.value}`);
    stocks = await rawStock.json();

    let html = '';
    stocks.forEach((stock, idx) => {
        html += `
        <div class="item">
            <img src="/static/assets/icons/${stock.nombre.replace(/ /g, "-")}.jpg" alt="${stock.nombre}"><br>
            <button class="order" onclick="solicitar(${idx})">solicitar</button>
            <div class="tooltip">
                <strong>${stock.nombre}</strong><br>
                Cantidad: ${stock.cantidad_disponible}<br>
            </div>
        </div>`;
    });
    document.getElementById("items-container").innerHTML = html;
}

renderizarStock();

