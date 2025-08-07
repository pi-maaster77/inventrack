async function renderizarPedidos() {
    rawPedidos = await fetch("/api/pedidos")
    pedidos = await rawPedidos.json()
    pedidos.forEach(pedido => {
        document.getElementById("content").innerHTML = ` 
        <div class="pedido-item">
            <h3>${pedido.nombre}</h3>
            <p><strong>Tamaño:</strong> ${pedido.tamano}</p>
            <p><strong>Cantidad:</strong> ${pedido.cantidad}</p>
            <p><strong>Hora de pedido:</strong> ${pedido.hora}</p>
            <p><strong>Hora de devolución:</strong> ${pedido.devolucion}</p>
        </div>`;
    });
}

renderizarPedidos()
setInterval(renderizarPedidos, 5000)