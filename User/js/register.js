console.log("JS cargado");

// Referencias
const user_register = document.getElementById("user_register");
const loginForm = document.getElementById("loginForm");
const btnRegister = document.getElementById("showRegister");
const btnLogin = document.getElementById("showLogin");
const btnLogout = document.getElementById("showLogout");

// Mostrar/ocultar formularios
btnRegister.addEventListener("click", () => {
  user_register.style.display = "block";
  loginForm.style.display = "none";
  btnLogout.style.display = "none";
});

btnLogin.addEventListener("click", () => {
  loginForm.style.display = "block";
  user_register.style.display = "none";
  btnLogout.style.display = "none";
});

// ------------------ REGISTER ------------------
user_register.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = {
    full_name: e.target.full_name.value,
    email: e.target.email.value,
    password: e.target.password.value
  };

  try {
    const res = await fetch("http://127.0.0.1:8000/register/", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(formData),
      credentials: "include"
    });

    const data = await res.json();
    if (res.ok) {
      alert(data.message);
      user_register.reset();
    } else {
      alert(data.error);
    }

  } catch (err) {
    alert("Error de conexión");
    console.error(err);
  }
});

// ------------------ LOGIN ------------------
loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = {
    email: e.target.email.value,
    password: e.target.password.value
  };

  try {
    const res = await fetch("http://127.0.0.1:8000/login/", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(formData),
      credentials: "include"
    });

    const data = await res.json();
    if (res.ok) {
      alert(data.message);
      loginForm.reset();
      loginForm.style.display = "none";
      user_register.style.display = "none";
      btnLogout.style.display = "inline-block";
    } else {
      alert(data.error);
    }

  } catch (err) {
    alert("Error de conexión");
    console.error(err);
  }
});

// ------------------ LOGOUT ------------------
// Botón logout
btnLogout.addEventListener("click", async () => {
  try {
    const res = await fetch("http://127.0.0.1:8000/logout/", {
      method: "POST",
      credentials: "include"
    });

    const contentType = res.headers.get("content-type");
    let data;

    if (contentType && contentType.includes("application/json")) {
      data = await res.json();
    } else {
      console.error("Respuesta inesperada del servidor:", await res.text());
      alert("Respuesta inesperada del servidor");
      return;
    }

    if (res.ok) {
      alert(data.message);
      window.location.href = "index.html";
    } else {
      alert(data.error || "Error inesperado");
    }

  } catch (err) {
    alert("Error de conexión");
    console.error(err);
  }
});

