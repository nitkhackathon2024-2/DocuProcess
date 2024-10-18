from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import easyocr
import spacy  # For advanced NLP processing
import json  # To save structured data as JSON
import fitz  # PyMuPDF for PDF text extraction

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

        # Save the structured data to a file
        structured_file_path = save_structured_data_to_file(structured_data, filename)
    
    # Check if the file is an image (png, jpg, etc.)
    elif filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        # Extract text from image using EasyOCR
        extracted_text = extract_text_from_image_using_easyocr(file_path)
        # Process extracted text into structured form
        structured_data = process_text_with_nlp(extracted_text['text'])

        # Save the structured data to a file
        structured_file_path = save_structured_data_to_file(structured_data, filename)
    
    else:
        return jsonify({"error": "Unsupported file type. Please upload an image or PDF file."}), 400

    return jsonify({"structured_data": structured_data, "structured_file": structured_file_path}), 200

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

# Process extracted text using NLP and structure it, with confidence heuristic
def process_text_with_nlp(extracted_text):
    # Run the NLP pipeline on the extracted text
    doc = nlp(extracted_text)

    # Example structured data initialization with confidence scores
    structured_data = {
        "person_names": [],
        "dates": [],
        "addresses": [],
        "organizations": [],
        "confidence": {}
    }

    # Simple heuristic: confidence score based on entity type
    entity_confidence = {
        "PERSON": 0.95,  # High confidence for PERSON
        "DATE": 0.9,
        "GPE": 0.85,
        "ORG": 0.9,
        "LOC": 0.85,
        "default": 0.75  # Lower confidence for other types
    }

    # Iterate over named entities to find people, dates, organizations, etc.
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            structured_data["person_names"].append(ent.text)
        elif ent.label_ == "DATE":
            structured_data["dates"].append(ent.text)
        elif ent.label_ == "GPE" or ent.label_ == "LOC":
            structured_data["addresses"].append(ent.text)
        elif ent.label_ == "ORG":
            structured_data["organizations"].append(ent.text)
        
        # Add confidence scores for each entity
        structured_data["confidence"][ent.text] = entity_confidence.get(ent.label_, entity_confidence["default"])

    return structured_data

# Save structured data to a JSON file
def save_structured_data_to_file(structured_data, original_filename):
    base_filename = os.path.splitext(original_filename)[0]
    structured_file_name = f"{base_filename}_structured.json"
    structured_file_path = os.path.join(app.config['UPLOAD_FOLDER'], structured_file_name)

    # Save the structured data to a JSON file
    with open(structured_file_path, 'w', encoding='utf-8') as f:
        json.dump(structured_data, f, ensure_ascii=False, indent=4)

    return structured_file_path

if __name__ == '__main__':
    app.run(debug=True)
