// Usuarios simulados
const usuarios = [
  { id:1, nombre:"Ana López", avatar:"https://i.pravatar.cc/40?img=5" },
  { id:2, nombre:"Carlos M.", avatar:"https://i.pravatar.cc/40?img=12" },
  { id:3, nombre:"Laura G.", avatar:"https://i.pravatar.cc/40?img=15" },
  { id:4, nombre:"Miguel R.", avatar:"https://i.pravatar.cc/40?img=20" }
];

// Usuario logueado
const usuarioActual = usuarios[0];

// Posts iniciales
let posts = [
  { id:1, usuario:usuarios[1], contenido:"¡Qué hermosa vista!", img:"https://picsum.photos/400/250?random=1", fecha:"2025-09-30 10:15", likes:5, comentarios:["Wow!","Hermoso!"] },
  { id:2, usuario:usuarios[2], contenido:"Disfrutando un café ☕", img:"https://picsum.photos/400/250?random=2", fecha:"2025-09-30 09:50", likes:3, comentarios:["Me encanta!"] },
  { id:3, usuario:usuarios[3], contenido:"Amando el otoño 🍁", img:"https://picsum.photos/400/250?random=3", fecha:"2025-09-29 18:30", likes:7, comentarios:[] }
];

let vistaActual = "home"; // home o perfil

// Crear nuevo post
function crearPost() {
  const input = document.getElementById("new-post");
  const texto = input.value.trim();
  if(texto==="") return;

  const nuevo = {
    id: posts.length + 1,
    usuario: usuarioActual,
    contenido: texto,
    img: `https://picsum.photos/400/250?random=${posts.length+10}`,
    fecha: new Date().toLocaleString(),
    likes:0,
    comentarios:[]
  };

  posts.unshift(nuevo);
  input.value="";
  mostrarPosts();
}

// Dar like
function darLike(id) {
  const post = posts.find(p=>p.id===id);
  post.likes++;
  mostrarPosts();
}

// Agregar comentario
function agregarComentario(id) {
  const texto = prompt("Escribe tu comentario:");
  if(!texto) return;
  const post = posts.find(p=>p.id===id);
  post.comentarios.push(texto);
  mostrarPosts();
}

// Mostrar posts según vista
function mostrarPosts() {
  const feed = document.getElementById("feed");
  feed.innerHTML="";

  let mostrar = vistaActual==="home" ? posts : posts.filter(p=>p.usuario.id===usuarioActual.id);

  mostrar.forEach(post=>{
    const div=document.createElement("div");
    div.className="post";

    div.innerHTML=`
      <div class="post-header" onclick="verPerfil(${post.usuario.id})">
        <img src="${post.usuario.avatar}">
        <div>
          <p class="name">${post.usuario.nombre}</p>
          <p class="date">${post.fecha}</p>
        </div>
      </div>
      <div class="post-content">
        <p>${post.contenido}</p>
        <img src="${post.img}">
      </div>
      <div class="post-actions">
        <button onclick="darLike(${post.id})">❤️ ${post.likes}</button>
        <button onclick="agregarComentario(${post.id})">💬 ${post.comentarios.length}</button>
      </div>
      ${post.comentarios.length>0 ? `<div class="comments">${post.comentarios.map(c=>`<p>• ${c}</p>`).join('')}</div>` : ''}
    `;

    feed.appendChild(div);
  });

  // Mostrar o esconder formulario
  document.getElementById("new-post-container").style.display = vistaActual==="perfil" ? "flex" : "none";
}

// Cambiar a perfil
function verPerfil(userId){
  if(userId===usuarioActual.id){
    vistaActual="perfil";
  } else {
    alert("Viendo perfil de otro usuario (solo posts visibles, no editable)");
    vistaActual="home"; // opcional: mantener home
  }
  mostrarPosts();
}

// Navegación
document.getElementById("nav-home").addEventListener("click", ()=>{
  vistaActual="home";
  mostrarPosts();
});
document.getElementById("nav-profile").addEventListener("click", ()=>{
  vistaActual="perfil";
  mostrarPosts();
});
document.getElementById("post-button").addEventListener("click", crearPost);

// Cargar inicial
document.addEventListener("DOMContentLoaded", mostrarPosts);