import os
import tempfile
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from chatbot import process_pdf, ask_question
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

vector_store = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    global vector_store
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file was uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file was selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    # Save to a temporary file instead of uploads folder
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        file.save(tmp_file.name)
        tmp_path = tmp_file.name
    
    try:
        vector_store = process_pdf(tmp_path)
        # Delete the temp file after processing
        os.unlink(tmp_path)
        return jsonify({'message': f'{file.filename} uploaded and processed successfully! You can now ask questions.'})
    except Exception as e:
        os.unlink(tmp_path)
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    global vector_store
    
    if vector_store is None:
        return jsonify({'error': 'Please upload a PDF first before asking questions'}), 400
    
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': 'Please type a question'}), 400
    
    answer = ask_question(vector_store, question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)