const usuario = document.getElementById("usuario");

async function validateToken(token) {
    const response = await fetch("/api/validate/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ token }),
    });
    return await response.json();
}

validateToken(localStorage.getItem("token")).then((response) => {
    if (!response.valid) {
        usuario.innerHTML = `
            <button onclick="location.href='/login'" class="login">Iniciar sesión</button>
            <button onclick="location.href='/register'" class="register">Registrarse</button>
        `;
        localStorage.removeItem("token");
    } else {
        usuario.textContent = `¡Hola ${response.user.nombre}!`;
    }
});
