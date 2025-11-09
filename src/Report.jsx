import React, { useState } from "react";
import "./report.css";

const ReportPost = () => {
  const [menuOpen, setMenuOpen] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [step, setStep] = useState(1);
  const [selectedReason, setSelectedReason] = useState("");
  const [details, setDetails] = useState("");

  const toggleMenu = () => setMenuOpen(!menuOpen);

  const openReportModal = () => {
    setModalOpen(true);
    setMenuOpen(false);
  };

  const handleReasonChange = (e) => {
    setSelectedReason(e.target.value);
  };

  const nextStep = () => {
    if (selectedReason) setStep(2);
  };

  const goBack = () => setStep(1);

  const closeModal = (e) => {
    if (e.target.className === "reportar") setModalOpen(false);
  };

  const handleSubmit = () => {
    console.log("Denuncia enviada:", {
      motivo: selectedReason,
      detalles: details,
    });
    setModalOpen(false);
    setStep(1);
    setSelectedReason("");
    setDetails("");
  };

  return (
    <div className="post-container">
      {/* Post */}
      <div className="post">
        <div className="menu" onClick={toggleMenu}>
          ⋮
        </div>

        {menuOpen && (
          <div className="menu-options">
            <button onClick={openReportModal}>Reportar</button>
            <button>Compartir</button>
          </div>
        )}
      </div>

      {/* Modal */}
      {modalOpen && (
        <div className="reportar" onClick={closeModal}>
          {step === 1 ? (
            <div className="opciones">
              <center><h2>Reportar Publicación</h2></center>
              <p>¿Qué sucede con la publicación?</p>

              <label className="option">
                <input
                  type="radio"
                  name="reason"
                  value="sexual"
                  onChange={handleReasonChange}
                  checked={selectedReason === "sexual"}
                />{" "}
                Contenido sexual
              </label>
              <label className="option">
                <input
                  type="radio"
                  name="reason"
                  value="violento"
                  onChange={handleReasonChange}
                  checked={selectedReason === "violento"}
                />{" "}
                Contenido violento o repulsivo
              </label>
              <label className="option">
                <input
                  type="radio"
                  name="reason"
                  value="odio"
                  onChange={handleReasonChange}
                  checked={selectedReason === "odio"}
                />{" "}
                Contenido abusivo o que incita al odio
              </label>
              <label className="option">
                <input
                  type="radio"
                  name="reason"
                  value="bullying"
                  onChange={handleReasonChange}
                  checked={selectedReason === "bullying"}
                />{" "}
                Acoso o bullying
              </label>
              <label className="option">
                <input
                  type="radio"
                  name="reason"
                  value="peligroso"
                  onChange={handleReasonChange}
                  checked={selectedReason === "peligroso"}
                />{" "}
                Actividades peligrosas o dañinas
              </label>
              <label className="option">
                <input
                  type="radio"
                  name="reason"
                  value="suicidio"
                  onChange={handleReasonChange}
                  checked={selectedReason === "suicidio"}
                />{" "}
                Suicidio, autolesiones o trastornos
              </label>

              <button
                className={`btn ${
                  selectedReason ? "btn-primary" : "btn-disabled"
                }`}
                disabled={!selectedReason}
                onClick={nextStep}
              >
                Siguiente
              </button>
            </div>
          ) : (
            <div className="mensaje">
              <span className="back" onClick={goBack}>
                ← Atrás
              </span>
              <h2>Reportar publicación</h2>
              <p>
                <b>¿Deseas brindar más información?</b> Este campo es opcional.
              </p>
              <textarea
                placeholder="Agrega detalles..."
                value={details}
                onChange={(e) => setDetails(e.target.value)}
              />
              <button className="btn btn-primary" onClick={handleSubmit}>
                Denunciar
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ReportPost;
