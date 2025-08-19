function cerrarCarrito() {
    const popup = document.getElementById('carrito');
    popup.classList.add('hidden');
    const body = document.getElementById('body');
    body.classList.remove('body-when-popup-showing');
}

function cerrarCantidad() {
    const popup = document.getElementById('cantidad');
    popup.classList.add('hidden');
    const body = document.getElementById('body');
    body.classList.remove('body-when-popup-showing');
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

