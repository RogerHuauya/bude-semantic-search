import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';
import teamImage from './assets/screenshot_20240615_142626.jpg'; // Asegúrate de poner la ruta correcta a la imagen

const Home = () => {
  const navigate = useNavigate();
  const submitHandler = () => { navigate('/query'); };

  return (
    <div className="home-container">
      <div className="header">
        <h1>Bienvenido a la Aplicacion de Indice invertido textual</h1>
      </div>
      <div className="content">
        <div className="team">
          <h2>Integrantes</h2>
          <ul>
            <li>Integrante 1</li>
            <li>Integrante 2</li>
            <li>Integrante 3</li>
            <li>Integrante 4</li>
            <li>Integrante 5</li>
            <li>Integrante 6</li>
          </ul>
          <img src={teamImage} alt="Team" className="team-image" />
        </div>
        <button className="start-button" onClick={submitHandler}>
          Iniciar
        </button>
      </div>
    </div>
  );
}

export default Home;
