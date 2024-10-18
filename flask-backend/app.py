from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import fitz  # PyMuPDF
import pytesseract
import easyocr

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set the upload folder path
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize EasyOCR reader (supports multiple languages if needed)
reader = easyocr.Reader(['en'])

# Route for uploading documents
@app.route('/upload', methods=['POST'])
def upload_document():
    print(request.files)  # Print all files in the request
    if 'file' not in request.files:
        return jsonify({"error": "No document uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Check if the file is a PDF
    if filename.lower().endswith('.pdf'):
        # Extract text from PDF using PyMuPDF and PyTesseract
        extracted_data = extract_text_from_pdf(file_path)
    elif filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        # Extract text from image using EasyOCR
        extracted_data = extract_text_from_image_using_easyocr(file_path)
    else:
        return jsonify({"error": "Unsupported file type. Please upload a PDF or image file."}), 400

    # Save the extracted data to a text file
    text_file_path = save_extracted_data_to_file(extracted_data['text'], filename)

    return jsonify({"extracted_data": extracted_data, "text_file": text_file_path}), 200

# Extract text from a PDF using PyMuPDF (fitz) and PyTesseract for OCR
def extract_text_from_pdf(file_path):
    pdf_document = fitz.open(file_path)
    text = ""
    
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)  # Load each page
        # Extract images from the page
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_path = os.path.join(UPLOAD_FOLDER, f"page_{page_num+1}_img_{img_index+1}.png")
            
            # Save image to the filesystem
            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)
            
            # Perform OCR on the saved image using PyTesseract
            text += pytesseract.image_to_string(image_path)
    
    pdf_document.close()
    
    return {"text": text}

# Extract text from an image using EasyOCR
def extract_text_from_image_using_easyocr(file_path):
    # Perform OCR using EasyOCR
    result = reader.readtext(file_path, detail=0)  # `detail=0` returns just the text
    text = " ".join(result)  # Join the extracted text into a single string
    return {"text": text}

# Save extracted data to a text file
def save_extracted_data_to_file(extracted_text, original_filename):
    base_filename = os.path.splitext(original_filename)[0]
    text_file_name = f"{base_filename}_extracted.txt"
    text_file_path = os.path.join(app.config['UPLOAD_FOLDER'], text_file_name)

    with open(text_file_path, 'w', encoding='utf-8') as text_file:
        text_file.write(extracted_text)

    return text_file_path

if __name__ == '__main__':
    app.run(debug=True)
