 document.getElementById("registro-form").addEventListener("submit", register);

async function login() {
    event.preventDefault(); // Evitar el envío del formulario por defecto
    const form = document.querySelector("form");
    const formData = new FormData(form);
    const messageSpan = document.getElementById("message");
    messageSpan.textContent = ""; // Limpiar mensaje previo

    const response = await fetch("/api/login/", {
        method: "POST",
        body: formData,
    });

    if (response.ok) {
        const result = await response.json();
        localStorage.setItem("token", result.token);
        messageSpan.textContent = "Inicio de sesión exitoso. Redirigiendo...";
        setTimeout(() => {
            window.location.href = "/";
        }, 1000); // Redirigir después de 1 segundo
    } else {
        const errorResult = await response.json();
        messageSpan.textContent = errorResult.error || "Error en el inicio de sesión.";
    }
    
}