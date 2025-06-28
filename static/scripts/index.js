async function renderizarStock() {
    busqueda = await document.getElementById("search-bar")
    rawStock = await fetch(`/api?search=${busqueda.value}`)

    stocks = await rawStock.json()
    stocks.forEach(stock => {
        document.getElementById("items-container").innerHTML = ` 
        <div class="item">
            <img src="/static/assets/${stock.imagen}" alt="${stock.nombre}"><br>
            <button class="order" onclick="solicitar(${stock})">solicitar</button>
            <div class="tooltip">
                <strong>${stock.nombre}</strong><br>
                Tamaño: ${stock.tamano}<br>
                Cantidad: ${stock.cantidad}<br>
                Ubicación: ${stock.ubicacion}
            </div>
        </div>`;
    });
}




renderizarStock()