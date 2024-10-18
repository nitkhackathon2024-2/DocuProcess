from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import fitz  # PyMuPDF
import requests  # For making requests to the Gemini API

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set the upload folder path
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        # Extract text from PDF
        extracted_data = extract_text_from_pdf(file_path)
    elif filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        # Extract text using the Gemini API for images
        extracted_data = extract_text_from_image_using_gemini(file_path)
    else:
        return jsonify({"error": "Unsupported file type. Please upload a PDF or image file."}), 400

    # Save the extracted data to a text file
    text_file_path = save_extracted_data_to_file(extracted_data['text'], filename)

    return jsonify({"extracted_data": extracted_data, "text_file": text_file_path}), 200

# Extract text from a PDF (using PyMuPDF)
def extract_text_from_pdf(file_path):
    pdf_document = fitz.open(file_path)
    text = ""
    
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)  # Load each page
        text += page.get_text("text")  # Extract text from each page

    pdf_document.close()

    return {"text": text}

# Extract text from an image using the Gemini API
def extract_text_from_image_using_gemini(file_path):
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyAWFG8qo8s3yohUBx32AzJ1z3Uph1BW0V8'  # Replace with your actual API key
    headers = {'Content-Type': 'application/json'}
    
    # Read the image file and encode it in base64 if required by the API
    with open(file_path, 'rb') as img_file:
        img_data = img_file.read()
    
    # Create the request payload
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": img_data.decode('latin-1')  # Encode the image data in a format the API accepts
                    }
                ]
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    # Print the response for debugging
    print("Gemini API Response:", response.json())

    if response.status_code == 200:
        response_data = response.json()

        # Adjust this based on the actual structure of the response
        if 'generated_text' in response_data:
            return {"text": response_data['generated_text']}  # Adjust the key based on the response
        else:
            return {"error": "Text not found in the response."}
    else:
        return {"error": "Failed to extract text from image using Gemini API"}


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
