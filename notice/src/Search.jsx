import './search.css';
import React, { useState } from 'react';


import { noticeData } from './data';

function Search({ onSearch }) {
    const [searchTerm, setSearchTerm] = useState('');

    const handleChange = (event) => {
        const value = event.target.value;
        setSearchTerm(value);
        const searchLower = value.trim().toLowerCase();
        const match =
            searchLower &&
            (noticeData.title.toLowerCase().includes(searchLower) ||
                noticeData.text.toLowerCase().includes(searchLower));
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