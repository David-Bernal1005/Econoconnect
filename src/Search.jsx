
import './search.css';
import React, { useState } from 'react';
import Notice from './Notice';


// Remove accents for search and highlight
function normalize(str) {
    // Remove accents using correct unicode range
    return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
}

function highlightText(text, searchTerm) {
    if (!searchTerm) return text;
    // Accent-insensitive highlight
    const normText = normalize(text);
    const normSearch = normalize(searchTerm);
    let result = '';
    let i = 0;
    while (i < text.length) {
        let found = false;
        for (let j = i + 1; j <= text.length; j++) {
            if (normalize(text.slice(i, j)) === normSearch) {
                result += `<mark style="background:#f1c40f;color:#232627;">${text.slice(i, j)}</mark>`;
                i = j;
                found = true;
                break;
            }
        }
        if (!found) {
            result += text[i];
            i++;
        }
    }
    return result;
}

function Search({ noticias = [], onSearch }) {
    const [searchTerm, setSearchTerm] = useState('');
    const [filteredNoticias, setFilteredNoticias] = useState([]);

    const handleChange = (event) => {
        const value = event.target.value;
        setSearchTerm(value);
        const searchLower = value.trim().toLowerCase();
            if (searchLower) {
                const normSearch = normalize(searchLower);
                const filtered = noticias.filter(n => {
                    const titulo = normalize(n.titulo || n.Titulo || '');
                    const resumen = normalize(n.resumen || n.Contenido || '');
                    const usuario = normalize(n.usuario || n.Usuario || '');
                    return titulo.includes(normSearch) || resumen.includes(normSearch) || usuario.includes(normSearch);
                });
                setFilteredNoticias(filtered);
                onSearch && onSearch({ match: filtered.length > 0, searching: true });
            } else {
                setFilteredNoticias([]);
                onSearch && onSearch({ match: false, searching: false });
            }
    };

        return (
            <div className="search-container">
                <div className="search">
                    <span className="search-icon"><img src="img/search.svg" alt="" /></span>
                    <input className="search-input" type="text" placeholder="Buscar noticia..." value={searchTerm} onChange={handleChange} />
                </div>
                {searchTerm && (
                    <div className="search-results" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', minHeight: '60vh', marginTop: '32px', gap: '32px' }}>
                        {filteredNoticias.length > 0 ? (
                            filteredNoticias.map((n, idx) => {
                                const titleRaw = n.titulo || n.Titulo || '';
                                const resumenRaw = n.resumen || n.Contenido || '';
                                const usuarioRaw = n.usuario || n.Usuario || '';
                                const searchLower = searchTerm.trim().toLowerCase();
                                const title = highlightText(titleRaw, searchLower);
                                const resumen = highlightText(resumenRaw, searchLower);
                                const usuario = highlightText(usuarioRaw, searchLower);
                                return (
                                    <div key={idx} className="search-result-item" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', width: '100%' }}>
                                        <div className="news-container" style={{ background: '#4c5058', borderRadius: '20px', margin: '0 auto', maxWidth: '660px', width: '100%' }}>
                                            <div className="sidebar">
                                                <button className="sidebar-button">Divisas</button>
                                                <button className="sidebar-button">M. Internacional</button>
                                                <button className="sidebar-button">Criptomonedas</button>
                                            </div>
                                            <div className="content">
                                                <div className="user-info">
                                                    <div className="avatar">
                                                        <img src="/img/profile.svg" alt="avatar" />
                                                    </div>
                                                    <span className="username" dangerouslySetInnerHTML={{ __html: usuario }} />
                                                </div>
                                                <div className="news-box">
                                                    <h3 className="news-title" dangerouslySetInnerHTML={{ __html: title }} />
                                                    <p className="news-text" dangerouslySetInnerHTML={{ __html: resumen }} />
                                                    {n.enlace && (
                                                        <a href={n.enlace} className="news-link" target="_blank" rel="noopener noreferrer">{n.enlace.replace(/^https?:\/\//, '').replace(/\/$/, '')}</a>
                                                    )}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                );
                            })
                        ) : (
                            <div className="search-result-item">No se encontraron noticias.</div>
                        )}
                    </div>
                )}
            </div>
        );
}

export default Search;


    // import React, { useState } from 'react';

    // function SearchBar({ onSearch }) {
    //   const [searchTerm, setSearchTerm] = useState('');

    //   const handleChange = (event) => {
    //     setSearchTerm(event.target.value);
    //     onSearch(event.target.value); // Pass the search term to a parent component or handler
    //   };

    //   return (
    //     <input
    //       type="text"
    //       placeholder="Search..."
    //       value={searchTerm}
    //       onChange={handleChange}
    //     />
    //   );
    // };

    // export default SearchBar;