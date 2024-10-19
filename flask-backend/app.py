from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import easyocr
import spacy  # For advanced NLP processing
import json  # To save structured data as JSON
import fitz  # PyMuPDF for PDF text extraction
import sqlite3  # Import SQLite3

app = Flask(__name__)
CORS(app)

# Create an upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Load a pre-trained spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Initialize SQLite database
DATABASE = 'structured_data.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            person_names TEXT,
            dates TEXT,
            addresses TEXT,
            organizations TEXT,
            confidence TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/upload', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Check if the file is a PDF
    if filename.lower().endswith('.pdf'):
        # Extract text from PDF using PyMuPDF
        extracted_text = extract_text_from_pdf(file_path)
        # Process extracted text into structured form
        structured_data = process_text_with_nlp(extracted_text['text'])

    # Check if the file is an image (png, jpg, etc.)
    elif filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        # Extract text from image using EasyOCR
        extracted_text = extract_text_from_image_using_easyocr(file_path)
        # Process extracted text into structured form
        structured_data = process_text_with_nlp(extracted_text['text'])
    
    else:
        return jsonify({"error": "Unsupported file type. Please upload an image or PDF file."}), 400

    # Save structured data to SQLite database
    save_structured_data_to_db(structured_data, filename)

    return jsonify({"structured_data": structured_data}), 200

# Extract text using EasyOCR (for images) with confidence values
def extract_text_from_image_using_easyocr(file_path):
    result = reader.readtext(file_path, detail=1)  # Enable detailed mode to get confidence scores
    text = " ".join([item[1] for item in result])  # Extract the text
    confidence = [item[2] for item in result]  # Extract the confidence scores
    return {"text": text, "confidence": confidence}

# Extract text from PDF using PyMuPDF
def extract_text_from_pdf(file_path):
    try:
        # Open the PDF file
        doc = fitz.open(file_path)
        text = ""

        # Iterate through pages and extract text
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text("text")  # Extract text from each page

        doc.close()
        return {"text": text}
    except Exception as e:
        return {"error": f"Error processing PDF: {str(e)}"}

# Process extracted text using NLP and structure it
def process_text_with_nlp(extracted_text):
    # Run the NLP pipeline on the extracted text
    doc = nlp(extracted_text)

    structured_data = {
        "person_names": [],
        "dates": [],
        "addresses": [],
        "organizations": [],
        "confidence": {}
    }

    # Base confidence heuristic
    base_confidence = {
        "PERSON": 0.85,  # Base confidence for PERSON
        "DATE": 0.8,     # Base confidence for DATE
        "GPE": 0.75,     # Base confidence for GPE
        "ORG": 0.8,      # Base confidence for ORG
        "LOC": 0.75,     # Base confidence for LOC
        "default": 0.65  # Default base confidence
    }

    # Confidence adjustment logic based on entity properties
    def adjust_confidence(entity, label):
        base_score = base_confidence.get(label, base_confidence["default"])

        # Increase confidence for well-formed entities
        if label == "PERSON":
            if len(entity.split()) > 1:  # If the name has more than one word (e.g., first + last name)
                return min(base_score + 0.1, 0.95)  # Cap at 0.95

        elif label == "DATE":
            # Check if it's a full date (e.g., contains both month and day)
            if any(char.isdigit() for char in entity) and any(char.isalpha() for char in entity):
                return min(base_score + 0.1, 0.9)

        elif label == "ORG":
            # If the organization ends with common suffixes (e.g., Inc., Ltd.)
            if any(suffix in entity for suffix in ["Inc.", "Ltd.", "LLC", "Corp.", "Company"]):
                return min(base_score + 0.1, 0.9)

        elif label in ["GPE", "LOC"]:
            # If it's a common location with multiple words (e.g., "New York")
            if len(entity.split()) > 1:
                return min(base_score + 0.1, 0.9)
        
        # If no specific conditions match, return the base confidence
        return base_score

    for ent in doc.ents:
        entity_text = ent.text
        entity_label = ent.label_

        # Classify the entity into structured data
        if entity_label == "PERSON":
            structured_data["person_names"].append(entity_text)
        elif entity_label == "DATE":
            structured_data["dates"].append(entity_text)
        elif entity_label == "GPE" or entity_label == "LOC":
            structured_data["addresses"].append(entity_text)
        elif entity_label == "ORG":
            structured_data["organizations"].append(entity_text)

        # Adjust confidence based on entity type and properties
        adjusted_confidence = adjust_confidence(entity_text, entity_label)
        structured_data["confidence"][entity_text] = adjusted_confidence

    return structured_data

# Save structured data to SQLite database
def save_structured_data_to_db(structured_data, original_filename):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Prepare data for insertion
    cursor.execute('''
        INSERT INTO documents (filename, person_names, dates, addresses, organizations, confidence) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        original_filename,
        ', '.join(structured_data['person_names']),
        ', '.join(structured_data['dates']),
        ', '.join(structured_data['addresses']),
        ', '.join(structured_data['organizations']),
        json.dumps(structured_data['confidence'])  # Save confidence as JSON string
    ))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()  # Initialize the database and create tables
    app.run(debug=True)
