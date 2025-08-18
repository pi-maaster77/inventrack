let stocks = []; // Variable global para acceder a los stocks

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

