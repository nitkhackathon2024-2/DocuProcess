# DocuProcess - Smart Document Processing

DocuProcess is a smart document processing platform that allows users to upload PDFs and images, extract key information using OCR (Optical Character Recognition) and NLP (Natural Language Processing), and view confidence scores for accuracy. It also offers features like auto-filling forms and document verification.

## Demo Video

Watch a demo of how DocuProcess works in the video below:

[![DocuProcess Demo](https://i9.ytimg.com/vi_webp/ZGlslA-L7-U/mq1.webp?sqp=CKClzLgG-oaymwEmCMACELQB8quKqQMa8AEB-AH-CYAC0AWKAgwIABABGFkgWShZMA8=&rs=AOn4CLDVQqaLPnraejQfte3_3QmaVyG1Bw)](https://www.youtube.com/watch?v=ZGlslA-L7-U)


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
```
## Setup Instructions
Prerequisites
Python 3.x
Node.js
npm or yarn

## Backend Setup (Flask)
```bash  
git clone https://github.com/nitkhackathon2024-2/DocuProcess.git
cd flask-backend
pip install -r requirements.txt
python app.py
```
The server will start running at http://127.0.0.1:5000/.

## Frontend Setup (React)
```bash
cd FormAPP
npm install
npm run dev
```
The frontend will run on http://localhost:3000/.

## API Endpoints
/upload (POST)
1) Description: Upload a document (PDF or image) for OCR and NLP processing.
2) Request: Multipart form data with the document file.
3) Response: JSON object with the structured data, including person names, dates, addresses, organizations, and confidence scores.


## Example
1) Go to the home page and click Upload Document.
2) Upload a PDF or image.
3) The platform extracts text and key information, presenting you with confidence scores and structured data.

### Contributors

This project was developed by 
[Sheldon Angelo Menezes](https://github.com/0x5h31d0n)
[Stalin Prevan Crasta](https://github.com/StalinPrevanCrasta)
[Jeswin Jacob Lobo](https://github.com/jeswin2003lobo)