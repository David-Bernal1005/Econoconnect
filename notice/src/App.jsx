import React, { useState } from 'react';
import Menu from './Menu';
import Search from './Search';
import Exit from './Exit';
import Carousel from './Carousel';
import Notice from './Notice';
import Filter from './Filter';
import './app.css';
import { noticeData } from './data';

const App = () => {
  const [match, setMatch] = useState(false);
  const [searching, setSearching] = useState(false);

  // Search le pasa si hay match y si está buscando
  const handleSearch = (result) => {
    setMatch(result.match);
    setSearching(result.searching);
  };

  return (
    <div className="main-layout">
      <aside>
        <Menu />
        <Exit />
        <Filter />
      </aside>
      <div className="main-content">
  <Search onSearch={handleSearch} />
        <section className="content-section">
          {searching ? (
            match ? <Notice /> : null
          ) : (
            <Carousel />
          )}
        </section>
      </div>
    </div>
  );
};

export default App;