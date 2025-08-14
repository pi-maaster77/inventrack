let stocks = []; // Variable global para acceder a los stocks

async function renderizarStock() {
    const busqueda = document.getElementById("search-bar");
    const rawStock = await fetch(`/api?search=${busqueda.value}`);
    stocks = await rawStock.json();

    let html = '';
    stocks.forEach((stock, idx) => {
        html += `
        <div class="item">
            <img src="/static/assets/${stock.nombre.replace(/ /g, "-")}.jpg" alt="${stock.nombre}"><br>
            <button class="order" onclick="solicitar(${idx})">solicitar</button>
            <div class="tooltip">
                <strong>${stock.nombre}</strong><br>
                Tamaño: ${stock.tamano}<br>
                Cantidad: ${stock.cantidad_disponible}<br>
            </div>
        </div>`;
    });
    document.getElementById("items-container").innerHTML = html;
}

function cerrarPopup() {
    const popup = document.getElementById('popup');
    popup.classList.add('hidden');
    const body = document.getElementById('body');
    body.classList.remove('body-when-popup-showing');
}

function solicitar(idx) {
    const herramienta = stocks[idx];
    console.log(`Solicitando herramienta: ${herramienta.nombre}`);
    const popup = document.getElementById('popup');
    popup.classList.remove('hidden');
    document.querySelector('.popup-title').textContent = `${herramienta.nombre}`;
    const body = document.getElementById('body');
    body.classList.add('body-when-popup-showing');
}

function increment() {
    const input = document.getElementById('integer-entry');
    input.value = parseInt(input.value) + 1;
}

function decrement() {
    const input = document.getElementById('integer-entry');
    input.value = Math.max(0, parseInt(input.value) - 1);
}

document.getElementById('integer-entry').addEventListener('input', function (e) {
    this.value = this.value.replace(/[^0-9]/g, '');
});

renderizarStock();

