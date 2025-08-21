let stocks

function nombreHttpCompatible(nombre) {
    // 1. Convertir a minúsculas
    nombre = nombre.toLowerCase();

    // 2. Eliminar acentos
    nombre = nombre.normalize("NFD").replace(/[\u0300-\u036f]/g, "");

    // 3. Reemplazar caracteres no válidos por guiones
    nombre = nombre.replace(/[^a-z0-9_.-]/g, "-");

    // 4. Reemplazar múltiples guiones consecutivos por uno solo
    nombre = nombre.replace(/-+/g, "-");

    // 5. Quitar guiones al inicio o final
    nombre = nombre.replace(/^-+|-+$/g, "");

    // 6. Escapar caracteres para URL
    nombre = encodeURIComponent(nombre);

    return nombre;
}

// Ejemplo de uso
console.log(nombreHttpCompatible("Mi foto #1.jpg"));
// Salida: mi-foto-1.jpg


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
                <img class="img" src="/static/assets/icons/${nombreHttpCompatible(stock.nombre)}.png" alt="${stock.nombre}"><br>
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
