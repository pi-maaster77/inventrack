let stocks

async function renderizarStock() {
    const busqueda = document.getElementById("search-bar");
    const rawStock = await fetch(`/api?search=${busqueda.value}`);
    stocks = await rawStock.json();

    let html = '';
    stocks.forEach((stock) => {
        const id = stock.id;
        html += `
        <div class="item">
            <div class="item-cotainer">
                <img src="/static/assets/icons/${stock.nombre.replace(/ /g, "-")}.jpg" alt="${stock.nombre}"><br>
                <button class="order" onclick="solicitar(${id})">Solicitar</button>
                <div class="solicitar-container hidden" id="item-${id}">
                    <input type="number" value="1" min="1" max="${stock.cantidad_disponible}" class="cantidad-input" id="cantidad-input-${id}">
                    <button class="agregar" onclick="anadir(${id})">Agregar</button>
                </div>
            </div>
            
            <div class="tooltip">
                <strong>${stock.nombre}</strong><br>
                Cantidad: ${stock.cantidad_disponible}<br>
            </div>
        </div>`;
    });

    document.getElementById("items-container").innerHTML = html;
}


function solicitar(id) {
    const container = document.getElementById(`item-${id}`);
    container.classList.toggle("hidden");
}




document.addEventListener("DOMContentLoaded", function() {
    renderizarStock();
});
