async function register() {
    event.preventDefault(); // Evitar el envío del formulario por defecto
    const form = document.querySelector("form");
    const formData = new FormData(form);
    const messageSpan = document.getElementById("message");
    messageSpan.innerHTML = ""; // Limpiar mensaje previo

    const response = await fetch("/api/registro/", {
        method: "POST",
        body: formData,
    });
    console.log(response);
    if (response.ok) {
        messageSpan.innerHTML = "Registro exitoso. Redirigiendo al inicio de sesión...";
        const result = await response.json();
        localStorage.setItem("token", result.token);
        setTimeout(() => {
            window.location.href = "/";
        }, 1000); // Redirigir después de 1 segundo
    } else {
        const errorResult = await response.json();
        messageSpan.textContent = errorResult.error || "Error en el registro.";
    }
    
}