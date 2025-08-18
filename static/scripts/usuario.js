usuarios = document.getElementById("usuario")

if(localStorage.getItem("usuario")) {
    usuarios.textContent = `Usuario: ${localStorage.getItem("usuario")}`;
} else {
    usuarios.innerHTML = `
    <button onclick="location.href='/login'" class="login">Iniciar sesión</button>
    <button onclick="location.href='/registro'" class="register">Registrarse</button>`;
}

