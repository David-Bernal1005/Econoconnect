 document.getElementById("loginForm").addEventListener("submit", async (e) => {
            e.preventDefault();
            
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;

            try {
                //fetch es el puente entre el frontend y el backend
                const res = await fetch("http://localhost:8000/api/v1/auth/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ username, password })
                });

                if (!res.ok) { 
                    throw new Error("Usuario o contraseña incorrectos");
                }

                const data = await res.json();
                localStorage.setItem("token", data.access_token);

                document.getElementById("message").innerText = "Inicio de sesión exitoso";
                window.location.href = "index.html"; // Redirigir
            } catch (err) {
                document.getElementById("message").innerText = err.message;
            }
        });
        