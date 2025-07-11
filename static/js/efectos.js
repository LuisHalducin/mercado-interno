document.addEventListener('DOMContentLoaded', () => {
  const texto = "Acceso autorizado: TRINITYX DOMINION conectado.";
  const contenedor = document.getElementById("acceso-texto");
  let i = 0;

  const escribir = () => {
    if (i < texto.length) {
      contenedor.textContent += texto.charAt(i);
      i++;
      setTimeout(escribir, 50);
    } else {
      // Agrega el cursor después del texto
      const cursor = document.createElement("span");
      cursor.classList.add("cursor");
      contenedor.appendChild(cursor);
    }
  };

  escribir();
});
