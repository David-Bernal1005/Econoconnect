import React from 'react';
import './notice.css';


import { noticeData } from './data';

const Notice = () => {
  return (
    <div className="news-container">
      <div className="sidebar">
        <button className="sidebar-button">Divisas</button>
        <button className="sidebar-button">M. Internacional</button>
        <button className="sidebar-button">Criptomonedas</button>
      </div>

      <div className="content">
        <div className="user-info">
          <div className="avatar"><img src='../public/img/profile.svg'/></div>
          <span className="username">Juan_088</span>
        </div>

        <div className="news-box">
          <h3 className="news-title">{noticeData.title}</h3>
          <p className="news-text">
            {noticeData.text}
          </p>
          <a href="https://interactivebrokers.com" className="news-link">Interactivebrokers.com</a>
        </div>
      </div>
    </div>
  );
};

export default Notice;
