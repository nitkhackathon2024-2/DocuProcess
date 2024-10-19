# DocuProcess - Smart Document Processing

DocuProcess is a smart document processing platform that allows users to upload PDFs and images, extract key information using OCR (Optical Character Recognition) and NLP (Natural Language Processing), and view confidence scores for accuracy. It also offers features like auto-filling forms and document verification.

## Demo Video

Watch a demo of how DocuProcess works in the video below:

[![DocuProcess Demo](https://i9.ytimg.com/vi_webp/ZGlslA-L7-U/mq1.webp?sqp=CKClzLgG-oaymwEmCMACELQB8quKqQMa8AEB-AH-CYAC0AWKAgwIABABGFkgWShZMA8=&rs=AOn4CLDVQqaLPnraejQfte3_3QmaVyG1Bw)](https://www.youtube.com/watch?v=ZGlslA-L7-U)

## College Name - Team Name
**College Name:** St. Joseph Engineering College  
**Team Name:** Extract0rs

## Team Members
- [Sheldon Angelo Menezes](https://github.com/0x5h31d0n)
- [Stalin Prevan Crasta](https://github.com/StalinPrevanCrasta)
- [Jeswin Jacob Lobo](https://github.com/jeswin2003lobo)

## Problem Statement
**Theme:** Smart Document Processing  
**Problem Statement:** Develop a platform that allows users to upload PDFs and images, extract key information using OCR and NLP, and provide confidence scores for accuracy. The platform should also offer features like auto-filling forms and document verification.

## Features

- **Easy Upload**: Upload and process PDFs and image files (JPG, PNG, etc.).
- **OCR & Data Extraction**: Extract text and key information automatically using EasyOCR and PyMuPDF.
- **Document Verification**: Verify the authenticity of uploaded documents.
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
│   ├── check_db.py              # Script to check database integrity or schema
│   ├── uploads/                 # Folder to store uploaded files
│   └── structured_data.db       # SQLite database for structured data
│
├── frontend/                    # Frontend React files
│   ├── public/                  # Public assets (HTML, etc.)
│   ├── src/
│       ├── components/          # Reusable React components
│       ├── HomePage.jsx         # Home page with upload and features
│       ├── Form.jsx             # Form component for data input and interaction
│       ├── App.jsx              # Main React component
│       ├── main.jsx             # Main entry point for the React app
│       ├── routes.jsx           # Routes for the different pages/components
│       ├── HomePage.css         # CSS file for styling the home page
│       ├── simpleForm.css       # CSS file for styling the form
│       └── index.css            # Global CSS file for the entire frontend
│
└── README.md                    # This README file
```

## Instructions on Running Your Project

### Prerequisites
- Python 3.x
- Node.js
- npm or yarn

### Backend Setup (Flask)
1. Clone the repository:
    ```bash
    git clone https://github.com/nitkhackathon2024-2/DocuProcess.git
    ```
2. Navigate to the backend directory:
    ```bash
    cd docuprocess/backend
    ```
3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the Flask server:
    ```bash
    python app.py
    ```
   The server will start running at `http://127.0.0.1:5000/`.

### Frontend Setup (React)
1. Navigate to the frontend directory:
    ```bash
    cd docuprocess/frontend
    ```
2. Install the required Node packages:
    ```bash
    npm install
    ```
3. Run the React development server:
    ```bash
    npm run dev
    ```
   The frontend will run on `http://localhost:3000/`.

## References
- [Flask Documentation](https://flask.palletsprojects.com/)
- [EasyOCR Documentation](https://www.jaided.ai/easyocr/)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [spaCy Documentation](https://spacy.io/)
- [React Documentation](https://reactjs.org/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

### Contributors

This project was developed by:
- [Sheldon Angelo Menezes](https://github.com/0x5h31d0n) - St. Joseph Engineering College
- [Stalin Prevan Crasta](https://github.com/StalinPrevanCrasta) - St. Joseph Engineering College
- [Jeswin Jacob Lobo](https://github.com/jeswin2003lobo) - St. Joseph Engineering College