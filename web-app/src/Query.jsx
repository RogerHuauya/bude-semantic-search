// import React, { useState } from 'react';
// import axios from "axios"
// import './Query.css';

// const Query = () => {
//     const [query, setQuery] = useState('');
//     const [topK, setTopK] = useState('');
//     const [selectedOption, setSelectedOption] = useState('');
//     const [result, setResult] = useState([]);
  
//     const handleInputChange = (event) => {
//       setQuery(event.target.value);
//     };
  
//     const handleTopKChange = (event) => {
//       setTopK(event.target.value);
//     };
  
//     const handleSelectChange = (event) => {
//       setSelectedOption(event.target.value);
//     };
  
//     const handleSubmit = (event) => {
//       event.preventDefault();
//       // Aquí puedes agregar la lógica para manejar la consulta
//       if( topK == '' | topK < 1){setTopK(1)}
//       var tmp =''
//       if(selectedOption == "postgres"){tmp = 'postgres-search';}
//       else if(selectedOption == "custom"){tmp = 'custom-search';}
//       let url = "http://localhost:8000/inverted-index/"+tmp+"/?query=%27"+query+"%27&k="+topK
      
//       axios.get(url)
//       .then(response => {
//           setResult(response.data);
//       })
//       .catch(error => {
//         setResult([]);
//       })
//       // setResult(`Resultado para: ${query} con top K = ${topK} y opción seleccionada = ${selectedOption}`);
//     };
  
//   return (
//     <div className="query-container">
//       <div className="main-content">
//         <h2>Query</h2>
//         <form onSubmit={handleSubmit}>
//           <textarea
//             value={query}
//             onChange={handleInputChange}
//             placeholder="Enter your natural language consult"
//             className='text-box'
//           />
//           <div className="form-footer">
//             <input
//               type="number"
//               value={topK}
//               onChange={handleTopKChange}
//               placeholder="top K"
//             />
//             <div className='selector'>
//               <select value={selectedOption} onChange={handleSelectChange}>
//                 <option value="" disabled>Metodo de Indexacion</option>
//                 <option value="postgres">Postgres</option>
//                 <option value="custom">Custom</option>
//               </select>
//             </div>
//             <div className='boton-execute'>
//               <button type="submit">Execute</button>
//             </div>
//           </div>
//         </form>
//       </div>
//       <div class="divider"></div>
//       <div className="result">
//           {result.length > 0 ? (
//             result.map((item, index) => (
//               <div key={index} className="result-item">
//                 <p><strong>Track ID:</strong> {item.track_id}</p>
//                 <p><strong>Track Name:</strong> {item.track_name}</p>
//                 <p><strong>Track Artist:</strong> {item.track_artist}</p>
//                 <p><strong>Lyrics:</strong> {item.lyrics}</p>
//                 <p><strong>Rank:</strong> {item.rank}</p>
//               </div>
//             ))
//           ) : (
//             <p>No results found</p>
//           )}
//       </div>
//         {/* {result && <div className="result">{result}</div>} */}
//     </div>
//   );
// }

// export default Query;

import sideImage1 from './assets/XiPu.gif'; // Asegúrate de poner la ruta correcta a la imagen


import React, { useState } from 'react';
import axios from "axios";
import './Query.css';

const Query = () => {
  const [query, setQuery] = useState('');
  const [topK, setTopK] = useState('');
  const [selectedOption, setSelectedOption] = useState('');
  const [result, setResult] = useState([]);

  const handleInputChange = (event) => {
    setQuery(event.target.value);
  };

  const handleTopKChange = (event) => {
    setTopK(event.target.value);
  };

  const handleSelectChange = (event) => {
    setSelectedOption(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (topK === '' || topK < 1) {
      setTopK(1);
    }
    let tmp = '';
    if (selectedOption === "postgres") {
      tmp = 'postgres-search';
    } else if (selectedOption === "custom") {
      tmp = 'custom-search';
    }
    let url = `http://localhost:8000/inverted-index/${tmp}/?query=${encodeURIComponent(query)}&k=${topK}`;

    axios.get(url)
      .then(response => {
        setResult(response.data);
      })
      .catch(error => {
        setResult([]);
      });
  };

  const downloadContent = () => {
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'result.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="query-container">
      <div className="main-content">
        <h2>Query</h2>
        <form onSubmit={handleSubmit}>
          <textarea
            value={query}
            onChange={handleInputChange}
            placeholder="Enter your natural language consult"
            className='text-box'
          />
          <div className="form-footer">
            <input
              type="number"
              value={topK}
              onChange={handleTopKChange}
              placeholder="top K"
            />
            <div className='selector'>
              <select value={selectedOption} onChange={handleSelectChange}>
                <option value="" disabled>Metodo de Indexacion</option>
                <option value="postgres">Postgres</option>
                <option value="custom">Custom</option>
              </select>
            </div>
            <div className='boton-execute'>
              <button type="submit">Execute</button>
            </div>
          </div>
        </form>
        <button onClick={downloadContent} className='boton-execute'>Download Content</button>
      </div>
      <div className="divider"></div>
      <div className="result">
        {result.length > 0 ? (
          result.map((item, index) => (
            <div key={index} className="result-item">
              <p><strong>Track ID:</strong> {item.track_id}</p>
              <p><strong>Track Name:</strong> {item.track_name}</p>
              <p><strong>Track Artist:</strong> {item.track_artist}</p>
              <p><strong>Lyrics:</strong> {item.lyrics}</p>
              <p><strong>Rank:</strong> {item.rank}</p>
            </div>
          ))
        ) : (
          <p>No results found</p>
        )}
      </div>
    </div>
  );
}

export default Query;
