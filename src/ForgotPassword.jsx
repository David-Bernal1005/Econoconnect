// ForgotPassword.jsx
import React, { useState } from "react";

export default function ForgotPassword() {
  const [step, setStep] = useState(1);
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [message, setMessage] = useState("");
  const [codeExpired, setCodeExpired] = useState(false);
  React.useEffect(() => {
    let timer;
    if (step === 2) {
      timer = setTimeout(() => {
        setCodeExpired(true);
        setMessage("El código ha expirado. Puedes solicitar uno nuevo.");
      }, 180000); // 3 minutos
    }
    return () => clearTimeout(timer);
  }, [step]);

  const handleRequestCode = async (e) => {
    e.preventDefault();
    setMessage("");
    setCodeExpired(false);
    const res = await fetch("http://localhost:8000/api/v1/auth/forgot-password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email })
    });
    if (res.ok) {
      setMessage("Código enviado al correo");
      setStep(2);
    } else {
      setMessage("No se encontró el usuario");
    }
  };

  const handleResetPassword = async (e) => {
    e.preventDefault();
    setMessage("");
    const res = await fetch("http://localhost:8000/api/v1/auth/reset-password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, code, new_password: newPassword })
    });
    if (res.ok) {
      setMessage("Contraseña actualizada");
      setStep(3);
    } else {
      const data = await res.json();
      setMessage(data.detail || "Error al cambiar la contraseña");
    }
  };

  return (
    <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", background: "#232627" }}>
      <div style={{ maxWidth: 420, width: "100%", background: "#fff6ea", borderRadius: 20, padding: 36, boxShadow: "0 4px 18px #23262733", border: "2px solid #f1c40f" }}>
        <h2 style={{ textAlign: "center", color: "#f1c40f", fontWeight: "bold", fontSize: 28, marginBottom: 24 }}>Recuperar contraseña</h2>
        {step === 1 && (
          <>
            <form onSubmit={handleRequestCode}>
              <label style={{ fontWeight: "bold", color: "#232627", fontSize: 16 }}>Correo electrónico</label>
              <input type="email" value={email} onChange={e => setEmail(e.target.value)} required style={{ width: "100%", marginBottom: 18, padding: 10, borderRadius: 8, border: "1.5px solid #f1c40f", fontSize: 15 }} />
              <button type="submit" style={{ background: "linear-gradient(90deg,#f1c40f,#ffd700)", color: "#232627", border: "none", borderRadius: 8, padding: "10px 0", fontWeight: "bold", cursor: "pointer", width: "100%", fontSize: 17, marginTop: 8, boxShadow: "0 2px 8px #f1c40f44" }}>Solicitar código</button>
            </form>
            <button onClick={() => window.location.href = "/login"} style={{ marginTop: 18, background: "#e0e0e0", color: "#232627", border: "none", borderRadius: 8, padding: "10px 0", fontWeight: "bold", cursor: "pointer", width: "100%", fontSize: 16 }}>Regresar al login</button>
          </>
        )}
        {step === 2 && (
          <>
            <form onSubmit={handleResetPassword}>
              <label style={{ fontWeight: "bold", color: "#232627", fontSize: 16 }}>Código recibido</label>
              <input type="text" value={code} onChange={e => setCode(e.target.value)} required style={{ width: "100%", marginBottom: 18, padding: 10, borderRadius: 8, border: "1.5px solid #f1c40f", fontSize: 15 }} disabled={codeExpired} />
              <label style={{ fontWeight: "bold", color: "#232627", fontSize: 16 }}>Nueva contraseña</label>
              <input type="password" value={newPassword} onChange={e => setNewPassword(e.target.value)} required style={{ width: "100%", marginBottom: 18, padding: 10, borderRadius: 8, border: "1.5px solid #f1c40f", fontSize: 15 }} disabled={codeExpired} />
              <button type="submit" style={{ background: "linear-gradient(90deg,#f1c40f,#ffd700)", color: "#232627", border: "none", borderRadius: 8, padding: "10px 0", fontWeight: "bold", cursor: codeExpired ? "not-allowed" : "pointer", width: "100%", fontSize: 17, marginTop: 8, boxShadow: "0 2px 8px #f1c40f44" }} disabled={codeExpired}>Cambiar contraseña</button>
            </form>
            {codeExpired && (
              <button onClick={handleRequestCode} style={{ marginTop: 18, background: "#f1c40f", color: "#232627", border: "none", borderRadius: 8, padding: "10px 0", fontWeight: "bold", cursor: "pointer", width: "100%", fontSize: 16 }}>Reenviar código</button>
            )}
            <button onClick={() => window.location.href = "/login"} style={{ marginTop: 18, background: "#e0e0e0", color: "#232627", border: "none", borderRadius: 8, padding: "10px 0", fontWeight: "bold", cursor: "pointer", width: "100%", fontSize: 16 }}>Regresar al login</button>
          </>
        )}
        {step === 3 && (
          <div style={{ textAlign: "center", color: "#388e3c", fontWeight: "bold", fontSize: 18, marginTop: 20 }}>
            <div style={{ marginBottom: 18 }}>¡Contraseña cambiada exitosamente!</div>
            <button onClick={() => window.location.href = "/login"} style={{ background: "linear-gradient(90deg,#f1c40f,#ffd700)", color: "#232627", border: "none", borderRadius: 8, padding: "10px 0", fontWeight: "bold", cursor: "pointer", width: "80%", fontSize: 17, boxShadow: "0 2px 8px #f1c40f44" }}>Ir al login</button>
          </div>
        )}
        {message && (
          <div style={{
            marginTop: 22,
            color:
              message === "Código enviado al correo"
                ? "#388e3c"
                : message.includes("actualizada")
                  ? "#388e3c"
                  : "#d32f2f",
            textAlign: "center",
            fontWeight: "bold",
            fontSize: 16
          }}>
            {message}
          </div>
        )}
      </div>
    </div>
  );
}
