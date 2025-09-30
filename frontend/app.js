const usuario = {
  id: 1,
  nombre: "Juan Pérez",
  avatar: "https://i.pravatar.cc/50?img=3"
};

function publicar() {
  const input = document.getElementById("mensaje");
  const posts = document.getElementById("posts");

  if (input.value.trim() === "") {
    alert("Escribe algo antes de publicar.");
    return;
  }

  const fecha = new Date().toLocaleString();
  const nuevoPost = document.createElement("div");
  nuevoPost.classList.add("post");

  nuevoPost.innerHTML = `
    <div class="author">
      <img src="${usuario.avatar}" style="width:30px; height:30px; border-radius:50%; vertical-align:middle; margin-right:5px;">
      ${usuario.nombre}
    </div>
    <div class="date">${fecha}</div>
    <p>${input.value}</p>
  `;

  posts.prepend(nuevoPost); // Nuevo post arriba
  input.value = "";
}
