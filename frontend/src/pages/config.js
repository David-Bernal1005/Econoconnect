function showContent(option) {
      const content = document.getElementById('content');
      document.querySelectorAll('.menu-item').forEach(item => item.classList.remove('active'));

      // --- Si el usuario selecciona la opción "Privacidad de la cuenta" ---
      if (option === 'perfil') {
        event.target.classList.add('active');
        content.innerHTML = `
          <h2>Privacidad de la cuenta</h2>
          <div class="toggle-container">
            <span>Cuenta privada</span>
            <label class="switch">
              <input type="checkbox" id="togglePerfil">
              <span class="slider"></span>
            </label>
          </div>
          <p>
            Si tu cuenta es pública, cualquiera podrá ver tu perfil y publicaciones, incluso quienes no tengan una cuenta.  
            Si tu cuenta es privada, solo los seguidores que apruebes podrán ver el contenido que compartas.
          </p>
        `;
      }
      // --- Si el usuario selecciona la opción "Privacidad de publicaciones" ---
      if (option === 'publicaciones') {
        event.target.classList.add('active');
        content.innerHTML = `
          <h2>Privacidad de publicaciones</h2>
          <div class="toggle-container">
            <span>Permitir que otros compartan mis publicaciones</span>
            <label class="switch">
              <input type="checkbox" id="toggleShare">
              <span class="slider"></span>
            </label>
          </div>
          <p>
            Si está activado, tus publicaciones podrán ser compartidas por otros usuarios en historias y mensajes.  
            Si está desactivado, nadie podrá compartir tu contenido directamente.
          </p>
          
          <div class="toggle-container">
            <span>¿Quién puede ver mis publicaciones?</span>
            <select id="postVisibility">
              <option value="todos">Todos</option>
              <option value="amigos">Amigos</option>
              <option value="solo">Solo yo</option>
            </select>
          </div>
          <p>
            Elige si quieres que tus publicaciones sean visibles para todos, solo tus amigos, o únicamente para ti.
          </p>
        `;
      }
    }