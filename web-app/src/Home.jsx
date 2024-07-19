// // //import React from 'react';
// // import {useNavigate} from 'react-router-dom';
// // import './Home.css';
// // import teamImage from './assets/screenshot_20240615_142626.jpg'; // Asegúrate de poner la ruta correcta a la imagen

// // const Home = () => {
// //     const navigate = useNavigate();
// //     const submitHandler = () => {
// //         navigate('/query');
// //     };

// //     return (
// //         <div className="home-container">
// //             <div className="header">
// //                 <h1>Bienvenido a la Aplicacion de Indice invertido textual</h1>
// //             </div>
// //             <div className="content">
// //                 <div className="team">
// //                     <h2>Integrantes</h2>
// //                     <ul>
// //                         <li>Roger Huauya Mamani</li>
// //                         <li>Arturo Barrantes Chuquimia</li>
// //                         <li>Angello Soldi Cataño</li>
// //                         <li>Rodrigo León Chumpitaz</li>
// //                         <li>Joel Jimenez Condori</li>
// //                     </ul>
// //                     <img src={teamImage} alt="Team" className="team-image"/>
// //                 </div>
// //                 <button className="start-button" onClick={submitHandler}>
// //                     Iniciar
// //                 </button>
// //             </div>
// //         </div>
// //     );
// // }

// // export default Home;


// import React from 'react';
// import { useNavigate } from 'react-router-dom';
// import './Home.css';
// import teamImage from './assets/screenshot_20240615_142626.jpg'; // Asegúrate de poner la ruta correcta a la imagen

// const Home = () => {
//     const navigate = useNavigate();
//     const submitHandler = () => {
//         navigate('/query');
//     };

//     return (
//         <div className="home-container">
//             <div className="header">
//                 <h1>Bienvenido a la Aplicación de Índice Invertido Textual</h1>
//             </div>
//             <div className="content">
//                 <div className="team">
//                     <h2>Integrantes</h2>
//                     <ul>
//                         <li>Roger Huauya Mamani</li>
//                         <li>Arturo Barrantes Chuquimia</li>
//                         <li>Angello Soldi Cataño</li>
//                         <li>Rodrigo León Chumpitaz</li>
//                         <li>Joel Jimenez Condori</li>
//                     </ul>
//                     <img src={teamImage} alt="Team" className="team-image" />
//                 </div>
//                 <button className="start-button" onClick={submitHandler}>
//                     Iniciar
//                 </button>
//             </div>
//         </div>
//     );
// }

// export default Home;




import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';
import teamImage from './assets/screenshot_20240615_142626.jpg'; // Asegúrate de poner la ruta correcta a la imagen
import sideImage1 from './assets/XiPu.gif'; // Asegúrate de poner la ruta correcta a la imagen
import sideImage2 from './assets/XiPu.gif'; // Asegúrate de poner la ruta correcta a la imagen

const Home = () => {
    const navigate = useNavigate();
    const submitHandler = () => {
        navigate('/query');
    };

    return (
        <div className="home-container">
            <div className="side-image-container">
                <img src={sideImage1} alt="Side 1" className="side-image" />
            </div>
            <div className="main-content">
                <div className="header">
                    <h1>Bienvenidos a Bude Semantic Search</h1>
                </div>
                <div className="content">
                    <div className="team">
                        <h2>Integrantes</h2>
                        <ul>
                            <li>Roger Huauya Mamani</li>
                            <li>Arturo Barrantes Chuquimia</li>
                            <li>Angello Soldi Cataño</li>
                            <li>Rodrigo León Chumpitaz</li>
                            <li>Joel Jimenez Condori</li>
                        </ul>
                        <img src={teamImage} alt="Team" className="team-image" />
                    </div>
                    <button className="start-button" onClick={submitHandler}>
                        Iniciar
                    </button>
                </div>
            </div>
            <div className="side-image-container">
                <img src={sideImage2} alt="Side 2" className="side-image" />
            </div>
        </div>
    );
}

export default Home;
