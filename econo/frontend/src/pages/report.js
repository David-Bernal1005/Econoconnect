const menu = document.querySelector('.menu');
  const menuOptions = document.querySelector('.menu-options');
  const reportBtn = document.getElementById('reportBtn');
  const reportModal = document.getElementById('reportModal');
  const nextBtn = document.getElementById('nextBtn');
  const backBtn = document.getElementById('backBtn');
  const denunciar = document.getElementById('denunciar');
  const atras = document.getElementById('atras');

  // Mostrar/ocultar menú
  menu.addEventListener('click', () => {
    menuOptions.style.display = menuOptions.style.display === 'block' ? 'none' : 'block';
  });

  // Abrir el reportaje
  reportBtn.addEventListener('click', () => {
    reportModal.style.display = 'flex';
    menuOptions.style.display = 'none';
  });

  // Selección de motivo
  document.querySelectorAll('input[name="reason"]').forEach(radio => {
    radio.addEventListener('change', () => {
      nextBtn.disabled = false;
      nextBtn.classList.remove('btn-disabled');
      nextBtn.classList.add('btn-primary');
    });
  });

  // Ir a escribir el comentario
  nextBtn.addEventListener('click', () => {
    denunciar.style.display = 'none';
    atras.style.display = 'block';
  });

  // Volver a las opciones
  backBtn.addEventListener('click', () => {
    denunciar.style.display = 'block';
    atras.style.display = 'none';
  });

  // Cerrar el reportaje al hacer clic fuera
  window.addEventListener('click', (e) => {
    if (e.target === reportModal) {
      reportModal.style.display = 'none';
    }
  });