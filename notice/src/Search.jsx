import './search.css';
import React, { useState } from 'react';


import { noticeData } from './data';

function Search({ onSearch }) {
    const [searchTerm, setSearchTerm] = useState('');
    const [apiResult, setApiResult] = useState(null);

    const handleChange = async (event) => {
        const value = event.target.value;
        setSearchTerm(value);
        const searchLower = value.trim().toLowerCase();
        let match = false;
        // Ejemplo: llamada a la API FastAPI para buscar usuarios
        if (searchLower) {
            try {
                const response = await fetch(`http://127.0.0.1:8000/api/v1/auth/search?username=${searchLower}`);
                if (response.ok) {
                    const data = await response.json();
                    setApiResult(data);
                    match = !!data && data.username && data.username.toLowerCase().includes(searchLower);
                } else {
                    setApiResult(null);
                }
            } catch (error) {
                setApiResult(null);
            }
        } else {
            setApiResult(null);
        }
        onSearch({ match: !!match, searching: !!searchLower });
    };

    return (
        <div className="search-container">
            <div className="search">
                <span className="search-icon"><img src="img/search.svg" alt=""/></span>
                <input className="search-input" type="text" placeholder="Search" value={searchTerm} onChange={handleChange}/>
            </div>
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