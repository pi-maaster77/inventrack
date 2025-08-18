async function renderizarPedidos() {
    const rawPedidos = await fetch("/api/pedidos", {
        method: "GET",
        headers: {
            "Authorization": localStorage.getItem("token")
        }
    });

    const prestamos = await rawPedidos.json();
    let html = "";

    prestamos.forEach((prestamo, index) => {
        html += `
        <div class="prestamo">
            <button class="accordion">📦 Préstamo: ${prestamo.fecha} 
                <span style="float:right">🕒 Devolución: ${prestamo.devolucion}</span>
            </button>
            <div class="panel">
                <ul>
                    ${prestamo.items.map(item => `<li>🔹 ${item.nombre} — ${item.cantidad}</li>`).join("")}
                </ul>
            </div>
        </div>`;
    });

    document.getElementById("content").innerHTML = html;
    activarAcordeones(); // Activa el comportamiento después de renderizar
}

function activarAcordeones() {
    const acc = document.getElementsByClassName("accordion");
    for (let i = 0; i < acc.length; i++) {
        acc[i].addEventListener("click", function () {
            this.classList.toggle("active");
            const panel = this.nextElementSibling;
            panel.style.display = panel.style.display === "block" ? "none" : "block";
        });
    }
}

renderizarPedidos();
