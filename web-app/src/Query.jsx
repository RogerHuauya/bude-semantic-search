import React, { useState } from 'react';
import './Query.css';

const Query = () => {
    const [query, setQuery] = useState('');
    const [topK, setTopK] = useState('');
    const [selectedOption, setSelectedOption] = useState('');
    const [result, setResult] = useState('');
  
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
      setResult(`Resultado para: ${query} con top K = ${topK} y opción seleccionada = ${selectedOption}`);
    };
  
  return (
    <div className="query-container">
      <div className="main-content">
        <h2>Consult</h2>
        <form onSubmit={handleSubmit}>
          <textarea
            value={query}
            onChange={handleInputChange}
            placeholder="Enter your natural language consult"
          />
          <div className="form-footer">
            <button type="submit">Execute</button>
            <input
              type="number"
              value={topK}
              onChange={handleTopKChange}
              placeholder="top K"
            />
            <select value={selectedOption} onChange={handleSelectChange}>
              <option value="" disabled>Metodo de Indexacion</option>
              <option value="option1">Option 1</option>
              <option value="option2">Option 2</option>
              <option value="option3">Option 3</option>
            </select>
          </div>
        </form>
        {result && <div className="result">{result}</div>}
      </div>
    </div>
  );
}

export default Query;
