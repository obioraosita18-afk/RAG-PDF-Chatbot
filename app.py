import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from chatbot import process_pdf, ask_question
from dotenv import load_dotenv

load_dotenv()

# Create our Flask web application
app = Flask(__name__)

# This is where uploaded PDF files will be saved
app.config['UPLOAD_FOLDER'] = 'uploads'

# Only allow PDF files to be uploaded
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# This stores our vector store in memory while the app is running
vector_store = None

def allowed_file(filename):
    """
    This function checks if the uploaded file is a PDF.
    We don't want people uploading random files!
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def home():
    """
    This is the home page of our chatbot.
    When someone visits our website this is what they see first.
    """
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_pdf():
    """
    This function handles PDF uploads.
    When the user uploads a PDF this function:
    1. Saves the PDF to our uploads folder
    2. Processes it into a vector store
    3. Returns a success message
    """
    global vector_store
    
    # Check if a file was actually sent
    if 'file' not in request.files:
        return jsonify({'error': 'No file was uploaded'}), 400
    
    file = request.files['file']
    
    # Check if a file was selected
    if file.filename == '':
        return jsonify({'error': 'No file was selected'}), 400
    
    # Check if it is a PDF
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    # Save the file safely
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Process the PDF and create vector store
    vector_store = process_pdf(filepath)
    
    return jsonify({'message': f'{filename} uploaded and processed successfully! You can now ask questions.'})


@app.route('/chat', methods=['POST'])
def chat():
    """
    This function handles questions from the user.
    When the user types a question this function:
    1. Gets the question
    2. Searches the vector store for relevant chunks
    3. Sends everything to LLaMA
    4. Returns the answer
    """
    global vector_store
    
    # Check if a PDF has been uploaded first
    if vector_store is None:
        return jsonify({'error': 'Please upload a PDF first before asking questions'}), 400
    
    # Get the question from the request
    data = request.get_json()
    question = data.get('question', '')
    
    # Check if a question was actually sent
    if not question:
        return jsonify({'error': 'Please type a question'}), 400
    
    # Get the answer from our chatbot
    answer = ask_question(vector_store, question)
    
    return jsonify({'answer': answer})


if __name__ == '__main__':
    app.run(debug=True)