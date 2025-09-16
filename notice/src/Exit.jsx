import React from "react";
import { Link } from "react-router-dom";
import "./exit.css";

const Exit = () => {
  return (
    <div className="sign-out">
      <Link to="/login">
        <img src="img/exit.svg" alt="Exit" />
      </Link>
    </div>
  );
};

export default Exit;
