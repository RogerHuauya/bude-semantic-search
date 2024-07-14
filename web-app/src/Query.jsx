import React, { useState } from 'react';
import axios from "axios"
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
      // Aquí puedes agregar la lógica para manejar la consulta
      if( topK == '' | topK < 1){setTopK(1)}
      var tmp =''
      if(selectedOption == "postgres"){tmp = 'postgres-search';}
      else if(selectedOption == "custom"){tmp = 'custom-search';}
      let url = "http://localhost:8000/inverted-index/"+tmp+"/?query=%27"+query+"%27&k="+topK
      
      axios.get(url)
      .then(response => {
          setResult(response.data);
      })
      .catch(error => {
        setResult([]);
      })
      // setResult(`Resultado para: ${query} con top K = ${topK} y opción seleccionada = ${selectedOption}`);
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
        {/* {result && <div className="result">{result}</div>} */}
      </div>
    </div>
  );
}

export default Query;
