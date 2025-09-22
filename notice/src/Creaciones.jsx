// Creaciones.jsx
import React, { useState } from "react";
import "./Creaciones.css";
import Menu from "./Menu";


export default function Creaciones() {
const [formData, setFormData] = useState({
	titulo: "",
	descripcion: "",
	soporte: "",
});


const allTags = [
"Renta Variable",
"Divisas",
"Criptomonedas",
"Noticias",
];


const [selectedTags, setSelectedTags] = useState([...allTags]);
const [mensaje, setMensaje] = useState("");


const handleChange = (e) => {
const { name, value } = e.target;
setFormData((prev) => ({ ...prev, [name]: value }));
};


const toggleTag = (tag) => {
setSelectedTags((prev) =>
prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag]
);
};


const handleSubmit = (e) => {
e.preventDefault();
const payload = { ...formData, etiquetas: selectedTags };
console.log("Enviando creación:", payload);
// Aquí iría la llamada al backend (fetch/axios)
setMensaje("✅ Creación guardada correctamente");
};


return (
<div className="creaciones-root">
	<div className="creaciones-layout">
		<aside className="creaciones-menu">
			<Menu />
		</aside>
		<div className="creaciones-container">
			<header className="creaciones-header">
				<div className="brand-pill">Creaciones</div>
			</header>
			<form className="creaciones-form" onSubmit={handleSubmit}>
				<div className="field">
					<label className="field-label">Título</label>
					<input
						className="input-title"
						name="titulo"
						value={formData.titulo}
						onChange={handleChange}
						placeholder="Escribe el título..."
					/>
				</div>
				<div className="field">
					<label className="field-label">Descripción</label>
					<textarea
						className="textarea-desc"
						name="descripcion"
						value={formData.descripcion}
						onChange={handleChange}
						placeholder="Escribe la descripción..."
					/>
				</div>
				<div className="field">
					<label className="field-label">Soporte</label>
					<div className="support-row">
						<input
							type="url"
							className="input-title"
							placeholder="Pega aquí la URL de soporte"
							value={formData.soporte}
							name="soporte"
							onChange={e => setFormData(prev => ({ ...prev, soporte: e.target.value }))}
						/>
					</div>
				</div>
				<div className="field">
					<label className="field-label">Etiquetas</label>
					<div className="tags">
						{allTags.map((t) => (
							<button
								key={t}
								type="button"
								className={`tag-pill ${selectedTags.includes(t) ? 'tag-active' : ''}`}
								onClick={() => toggleTag(t)}
							>
								<span className="tag-x">×</span>
								<span className="tag-text">{t}</span>
							</button>
						))}
					</div>
				</div>
				<div className="actions">
					{mensaje && <div className="mensaje">{mensaje}</div>}
				</div>
			</form>
		</div>
						<button className="btn-publish" onClick={e => { e.preventDefault(); handleSubmit(e); }}>Publicar</button>

	</div>
</div>
);
}