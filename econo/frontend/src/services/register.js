document.getElementById("registerForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const data = {
        name: document.getElementById("usua_nombre").value,
        lastname: document.getElementById("usua_apellido").value,
        cellphone: Number(document.getElementById("usua_celular").value),
        direction: document.getElementById("usua_direccion").value,
        country: document.getElementById("usua_pais").value,
        username: document.getElementById("usua_usuario").value,
        password: document.getElementById("usua_password").value,
        rol: document.getElementById("usua_rol_fk").value,
        email: document.getElementById("usua_email").value
    };

            try {
                const response = await fetch("http://localhost:8000/api/v1/auth/register", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(data)
                });

                const result = await response.json();
                if (response.ok) {
                    document.getElementById("mensaje").innerText = "Usuario registrado con éxito 🎉";
                } else {
                    let errorMsg = result.detail || JSON.stringify(result);
                    document.getElementById("mensaje").innerText = "Error: " + errorMsg;
                }
            } catch (err) {
                document.getElementById("mensaje").innerText = "Error en el servidor";
            }
        });