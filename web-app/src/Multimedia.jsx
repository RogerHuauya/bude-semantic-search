import React, { useState, useRef, useEffect } from 'react';
import axios from "axios";
import './Multimedia.css';

const Multimedia = () => {
  const [topK, setTopK] = useState('');
  const [selectedOption, setSelectedOption] = useState('');
  const [result, setResult] = useState([]);
  const [file, setFile] = useState(null);
  const [showAttributes, setShowAttributes] = useState({
    id: true,
    title: true,
    article_type: true,
    base_colour: true,
    gender: true,
    master_category: true,
    product_display_name: true,
    season: true,
    sub_category: true,
    usage: true,
    year: true,
  });
  const [cameraEnabled, setCameraEnabled] = useState(false);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);


  useEffect(() => {
    if (cameraEnabled && videoRef.current) {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
          videoRef.current.srcObject = stream;
        })
        .catch(err => {
          console.error('Error accessing camera:', err);
        });
    }
  }, [cameraEnabled]);


  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleTopKChange = (event) => {
    setTopK(event.target.value);
  };

  const handleSelectChange = (event) => {
    setSelectedOption(event.target.value);
  };

  const handleCheckboxChange = (event) => {
    const { name, checked } = event.target;
    setShowAttributes((prevState) => ({
      ...prevState,
      [name]: checked,
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (topK === '' || topK < 1) {
      setTopK(1);
    }

    let tmp = '';
    if (selectedOption === "postgres") {
      tmp = 'postgres-search';
    } else if (selectedOption === "sequential") {
      tmp = 'sequential-search';
    } else if (selectedOption === "rtree") {
      tmp = 'rtree-search';
    }

    const formData = new FormData();
    formData.append('query_image', file);
    formData.append('count', topK);
    formData.append('serial', '6101362862');

    axios.post('http://localhost:8000/image/image/search/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    .then(response => {
      console.log('File uploaded successfully', response.data);
      setResult(response.data);
    })
    .catch(error => {
      console.error('There was an error uploading the file!', error);
    });
  };

  const enableCamera = () => {
    setCameraEnabled(true);
  };

  const takePhoto = () => {
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');
    context.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
    canvas.toBlob(blob => {
      const file = new File([blob], 'photo.jpg', { type: 'image/jpeg' }); // Crear el archivo con la extensión correcta
      setFile(file);
      setCameraEnabled(false);
    }, 'image/jpeg');
  };

  return (
    <div className="query-container">
      <div className="main-content">
        <h2>Query</h2>
        <div className="form-footer">
          <form onSubmit={handleSubmit}>
            <input type="file" onChange={handleFileChange} className='file-up'/>
            <div className='bye'>
              <button type="button" onClick={enableCamera} >Enable Camera</button>
            </div>
            {cameraEnabled && (
              <div className='video-rref'>
                <video ref={videoRef} autoPlay width="300" height="200"></video>
                <button type="button" onClick={takePhoto} className='bye'>Take Photo</button>
                <canvas ref={canvasRef} width="300" height="200" style={{ display: 'none' }}></canvas>
              </div>
            )}
            <input type="number" value={topK} onChange={handleTopKChange} placeholder="top K" className='i-num'/>
            <div className='selector'>
              <select value={selectedOption} onChange={handleSelectChange}>
                <option value="" disabled>Metodo de Indexacion</option>
                <option value="postgres">Postgres</option>
                <option value="sequential">Sequential</option>
                <option value="rtree">Rtree</option>
              </select>
            </div>
            <div className='boton-execute'>
              <button type="submit">Execute</button>
            </div>
          </form>
          {Object.keys(showAttributes).map((attribute) => (
            <div key={attribute}>
              <input
                type="checkbox"
                name={attribute}
                checked={showAttributes[attribute]}
                onChange={handleCheckboxChange}
              />
              <label>{attribute.replace('_', ' ').toUpperCase()}</label>
            </div>
          ))}
        </div>
        <div className="result">
          {result.length > 0 ? (
            result.map((item, index) => (
              <div key={index} className="result-item">
                <img src={item.image_file} alt={item.title} />
                {showAttributes.id && <p><strong>ID:</strong> {item.id}</p>}
                {showAttributes.title && <p><strong>Title:</strong> {item.title}</p>}
                {showAttributes.article_type && <p><strong>Article Type:</strong> {item.article_type}</p>}
                {showAttributes.base_colour && <p><strong>Base Colour:</strong> {item.base_colour}</p>}
                {showAttributes.gender && <p><strong>Gender:</strong> {item.gender}</p>}
                {showAttributes.master_category && <p><strong>Master Category:</strong> {item.master_category}</p>}
                {showAttributes.product_display_name && <p><strong>Product Display Name:</strong> {item.product_display_name}</p>}
                {showAttributes.season && <p><strong>Season:</strong> {item.season}</p>}
                {showAttributes.sub_category && <p><strong>Sub Category:</strong> {item.sub_category}</p>}
                {showAttributes.usage && <p><strong>Usage:</strong> {item.usage}</p>}
                {showAttributes.year && <p><strong>Year:</strong> {item.year}</p>}
              </div>
            ))
          ) : (
            <p>No results found</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Multimedia;
