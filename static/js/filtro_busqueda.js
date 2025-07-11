document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('busqueda');
  if (!input) return;

  const tarjetas = document.querySelectorAll('.tarjeta');

  // FILTRO POR PRODUCTO
  input.addEventListener('input', () => {
    const valor = input.value.toLowerCase();
    tarjetas.forEach(tarjeta => {
      const producto = tarjeta.dataset.producto || '';
      console.log('producto:', producto, 'buscando:', valor);
      if (producto.includes(valor)) {
        tarjeta.style.display = 'block';
      } else {
        tarjeta.style.display = 'none';
      }
    });
  });

  // MODAL PARA AGRANDAR TARJETA
  const modal = document.getElementById('modal');
  const modalDetalle = document.getElementById('modal-detalle');
  const btnCerrar = document.getElementById('cerrar-modal');

  tarjetas.forEach(tarjeta => {
    tarjeta.addEventListener('click', () => {
      // Copiar el contenido de la tarjeta al modal
      modalDetalle.innerHTML = tarjeta.innerHTML;
      modal.style.display = 'block';
    });
  });

  btnCerrar.addEventListener('click', () => {
    modal.style.display = 'none';
  });

  window.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.style.display = 'none';
    }
  });
});
