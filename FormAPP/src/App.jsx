import React, { useState, useRef, useEffect } from 'react';

const App = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [imageData, setImageData] = useState(null);
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [extractedData, setExtractedData] = useState(null);

  useEffect(() => {
    navigator.mediaDevices
      .getUserMedia({
        video: {
          facingMode: { ideal: 'environment' },
        },
      })
      .then((stream) => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      })
      .catch((err) => {
        console.error('Error accessing the camera:', err);
      });
  }, []);

  const captureImage = () => {
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');
    context.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
    const imageUrl = canvas.toDataURL('image/png');
    setImageData(imageUrl);
    setFile(null);
  };

  const handleFileChange = (e) => {
    const uploadedFile = e.target.files[0];
    if (uploadedFile) {
      setFile(uploadedFile);
      setImageData(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const selectedFile = file || (imageData ? await fetch(imageData).then((res) => res.blob()) : null);

    if (!selectedFile) {
      setMessage('Please capture an image or upload a file!');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile, selectedFile.name || 'captured_image.png');

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      if (!response.ok) {
        throw new Error(result.error || 'File upload failed.');
      }

      setMessage(result.message || 'File uploaded successfully! Check server logs for more.');
      if (result.structured_data) {
        setExtractedData(result.structured_data); // Store extracted data
      }
    } catch (error) {
      console.error('Error uploading the file:', error);
      setMessage('Failed to upload image.');
    }
  };

  const getConfidenceClass = (confidence) => {
    if (confidence >= 0.9) return 'verified';
    if (confidence >= 0.75) return 'unverified';
    return 'low-confidence';
  };

  return (
    <div className="App">
      <h1>Smart Document Processor</h1>
      <video ref={videoRef} autoPlay playsInline style={{ width: '100%', height: 'auto' }}></video>
      <canvas ref={canvasRef} width={640} height={480} style={{ display: 'none' }}></canvas>
      <button onClick={captureImage}>Capture Image</button>
      {imageData && (
        <div>
          <h3>Captured Image</h3>
          <img src={imageData} alt="Captured" />
        </div>
      )}
      <div>Or</div>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      <form onSubmit={handleSubmit}>
        <button type="submit">Upload Image</button>
      </form>
      {message && <p>{message}</p>}

      {extractedData && (
        <div>
          <h3>Extracted Data</h3>
          <ul>
            {extractedData.person_names.map((name) => (
              <li key={name} className={getConfidenceClass(extractedData.confidence[name])}>
                {name} - Confidence: {extractedData.confidence[name]}
              </li>
            ))}
            {extractedData.dates.map((date) => (
              <li key={date} className={getConfidenceClass(extractedData.confidence[date])}>
                {date} - Confidence: {extractedData.confidence[date]}
              </li>
            ))}
            {extractedData.organizations.map((org) => (
              <li key={org} className={getConfidenceClass(extractedData.confidence[org])}>
                {org} - Confidence: {extractedData.confidence[org]}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default App;
