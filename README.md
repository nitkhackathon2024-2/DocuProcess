# DocuProcess - Smart Document Processing

DocuProcess is a smart document processing platform that allows users to upload PDFs and images, extract key information using OCR (Optical Character Recognition) and NLP (Natural Language Processing), and view confidence scores for accuracy. It also offers features like auto-filling forms and document verification.

## Features

- **Easy Upload**: Upload and process PDFs and image files (JPG, PNG, etc.).
- **OCR & Data Extraction**: Extract text and key information automatically using EasyOCR and PyMuPDF.
- **Document Verification**: Verify the authenticity of uploaded documents.
- **Auto-fill Forms**: Instantly populate forms with extracted data.
- **Confidence Scores**: View confidence levels for extracted data for accuracy.
- **Secure Processing**: All data is securely stored in SQLite3.

## Tech Stack

### Backend
- **Flask**: Lightweight web framework for the server-side logic.
- **EasyOCR**: Used for extracting text from image files.
- **PyMuPDF (fitz)**: Used for extracting text from PDF files.
- **spaCy**: NLP model to process and extract structured data such as names, dates, and organizations.
- **SQLite3**: Database for storing structured data and ensuring data security.

### Frontend
- **React.js**: User interface for the application.
- **Lucide React**: Icons for visual elements.
- **CSS**: Styling the React components.

## Project Structure

```bash
docuprocess/
│
├── backend/                     # Backend files
│   ├── app.py                   # Flask server with OCR and NLP processing
│   ├── uploads/                 # Folder to store uploaded files
│   └── structured_data.db       # SQLite database for structured data
│
├── frontend/                    # Frontend React files
│   ├── public/                  # Public assets (HTML, etc.)
│   ├── src/
│       ├── components/          # Reusable React components
│       ├── HomePage.jsx         # Home page with upload and features
│       ├── App.jsx              # Main React component
│       └── HomePage.css         # CSS file for styling the home page
│
└── README.md                    # This README file