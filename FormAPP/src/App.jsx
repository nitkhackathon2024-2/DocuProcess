import React, { useState, useRef, useEffect } from 'react';

const App = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [imageData, setImageData] = useState(null);
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');

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
      if (result.extracted_data) {
        setMessage(`Extracted Text: ${result.extracted_data.text}`);
      }
    } catch (error) {
      console.error('Error uploading the file:', error);
      setMessage('Failed to upload image.');
    }
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
    </div>
  );
};

export default App;
