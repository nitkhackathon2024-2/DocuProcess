import React from 'react';
import { useNavigate } from 'react-router-dom'; // useNavigate instead of useHistory
import { Upload, FileText, CheckCircle, FileInput, BarChart3, Lock } from 'lucide-react';
import './HomePage.css';

function HomePage() {
  const navigate = useNavigate(); // Updated hook for navigation

  const handleNavigateToUpload = () => {
    navigate('/upload'); // Navigate to /upload (App.jsx)
  };

  return (
    <div className="container">
      {/* Header Section */}
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <FileText className="icon" />
            <span className="logo-text">DocuProcess</span>
          </div>
          <nav>
            <ul className="nav-links">
              <li><a href="#">Home</a></li>
              <li><a href="#" onClick={handleNavigateToUpload}>Upload</a></li> {/* Link to upload page */}
              <li><a href="SimpleForm">Form</a></li>
            </ul>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="main">
        <div className="main-content">
          <div className="intro">
            <h1 className="title">Smart Document Processing</h1>
            <p className="subtitle">
              Upload your documents, extract information automatically, and view confidence scores for accuracy.
            </p>

            {/* Button to navigate to the upload page */}
            <div className="button-wrapper">
              <button className="upload-button" onClick={handleNavigateToUpload}>
                <Upload className="button-icon" />
                Upload Document
              </button>
            </div>
          </div>

          {/* Key Features Section */}
          <div className="features">
            <h2 className="features-title">Key Features</h2>
            <div className="features-grid">
              <FeatureCard
                icon={<Upload className="feature-icon" />}
                title="Easy Upload"
                description="Drag and drop your PDFs and images for quick processing."
              />
              <FeatureCard
                icon={<FileText className="feature-icon" />}
                title="OCR & Data Extraction"
                description="Extract text and key information from your documents automatically."
              />
              <FeatureCard
                icon={<CheckCircle className="feature-icon" />}
                title="Document Verification"
                description="Verify the authenticity and integrity of your uploaded documents."
              />
              <FeatureCard
                icon={<FileInput className="feature-icon" />}
                title="Auto-fill Forms"
                description="Populate forms instantly with extracted data, saving you time."
              />
              <FeatureCard
                icon={<BarChart3 className="feature-icon" />}
                title="Confidence Scores"
                description="View confidence levels for extracted data to ensure accuracy."
              />
              <FeatureCard
                icon={<Lock className="feature-icon" />}
                title="Secure Processing and Storage"
                description="Data Highly Secured as it is stored in sqlite3 DB"
              />
            </div>
          </div>
        </div>
      </main>

      {/* Footer Section */}
      <footer className="footer">
        <div className="footer-content">
          <div className="footer-links">
            <a href="#">Privacy Policy</a>
            <a href="#">Terms of Service</a>
            <a href="#">Contact</a>
          </div>
          <div className="footer-text">
            <p>&copy; 2023 DocuProcess. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

// FeatureCard component
function FeatureCard({ icon, title, description }) {
  return (
    <div className="feature-card">
      <div className="feature-icon-wrapper">
        {icon}
      </div>
      <h3 className="feature-title">{title}</h3>
      <p className="feature-description">{description}</p>
    </div>
  );
}

export default HomePage;
