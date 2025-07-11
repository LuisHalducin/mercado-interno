function openTab(evt, tabId) {
  const tabContents = document.querySelectorAll('.tab-content');
  const tabButtons = document.querySelectorAll('.tab-button');
  
  tabContents.forEach(tc => tc.style.display = 'none');
  tabButtons.forEach(tb => tb.classList.remove('active'));
  
  document.getElementById(tabId).style.display = 'block';
  evt.currentTarget.classList.add('active');
}

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
