let listaDeSolicitudes = [];

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
                <button class="order" onclick="solicitar(${id})">solicitar</button>
                <div class="solicitar-container hidden" id="item-${id}">
                    <input type="number" value="1" min="1" class="cantidad-input" id="cantidad-input-${id}">
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

function anadir(id) {
    const cantidadInput = document.getElementById(`cantidad-input-${id}`);
    const cantidad = parseInt(cantidadInput.value, 10);

    if (isNaN(cantidad) || cantidad < 1) {
        console.error("Cantidad inválida");
        return;
    }

    const herramienta = stocks.find(s => s.id === id);
    if (!herramienta) {
        console.error(`No se encontró la herramienta con ID ${id}`);
        return;
    }

    const existente = listaDeSolicitudes.find(item => item.id === id);
    if (existente) {
        existente.cantidad += cantidad;
    } else {
        listaDeSolicitudes.push({ id: id, cantidad });
    }

    console.log(listaDeSolicitudes);
    renderizarSolicitudes();
}

function actualizarCantidad(idx) {
    const pedido = listaDeSolicitudes[idx];
    const input = document.getElementById(`cantidad-carrito-${pedido.id}`);
    const nuevaCantidad = parseInt(input.value, 10);

    if (!isNaN(nuevaCantidad) && nuevaCantidad >= 1) {
        pedido.cantidad = nuevaCantidad;
        console.log(`Cantidad actualizada para ID ${pedido.id}: ${nuevaCantidad}`);
    } else {
        console.error("Cantidad inválida.");
        input.value = pedido.cantidad; // Restaurar valor anterior
    }
}

function eliminarPedido(idx) {
    listaDeSolicitudes.splice(idx, 1);
    console.log(`Solicitud eliminada: Índice ${idx}`);
    renderizarSolicitudes();
}

async function enviarPedido() {
    event.preventDefault();
    const token = localStorage.getItem("token");
    if (!token) {
        console.error("No se encontró el token de sesión.");
        return;
    }
    const response = await fetch("/api/solicitar/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            token: token,
            solicitudes: listaDeSolicitudes
        })
    });
    if (response.ok) {
        const data = await response.json();
        alert(`Pedido enviado exitosamente: ${data.message}`);
        listaDeSolicitudes = [];
        renderizarSolicitudes();
    } else {
        console.error("Error al enviar el pedido:", response.statusText);
    }
}

async function renderizarSolicitudes() {
    const listaPedidos = document.getElementById("lista-pedidos");
    listaPedidos.innerHTML = '';

    listaDeSolicitudes.forEach((pedido, idx) => {
        const herramienta = stocks.find(item => item.id === pedido.id);
        const nombre = herramienta ? herramienta.nombre : "Nombre no encontrado";

        listaPedidos.innerHTML += `<li>
            <span>${nombre}</span>
            <input type="number" 
                value="${pedido.cantidad}" 
                min="1" 
                class="cantidad-carrito" 
                id="cantidad-carrito-${pedido.id}" 
                onchange="actualizarCantidad(${idx})">
            <button onclick="eliminarPedido(${idx})">Eliminar</button>
        </li>`;
    });
}

function toggleCarrito() {
    const popup = document.getElementById('carrito');
    popup.classList.toggle('hidden');
    const body = document.getElementById('body');
    body.classList.toggle('body-when-popup-showing');
    renderizarSolicitudes();
}

document.addEventListener("DOMContentLoaded", () => {
    renderizarStock();
});
