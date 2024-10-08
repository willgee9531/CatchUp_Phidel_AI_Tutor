import os
# import requests
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from docx import Document
import json
# import openai
from g4f.client import Client
from config import Config

"""
# Set up proxy for PythonAnywhere
os.environ['HTTP_PROXY'] = 'http://proxy.server:3128'
os.environ['HTTPS_PROXY'] = 'http://proxy.server:3128'

# Configure requests to use the proxy
proxies = {
    'http': 'http://proxy.server:3128',
    'https': 'http://proxy.server:3128'
}
"""

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def save_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(os.getcwd(), Config.UPLOAD_FOLDER)
        
        # Create the upload folder if it doesn't exist
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        return filepath
    return None

def extract_text(filepath):
    _, extension = os.path.splitext(filepath)
    
    if extension == '.txt':
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    elif extension == '.pdf':
        with open(filepath, 'rb') as file:
            pdf = PdfReader(file)
            text = ""
            for page in pdf.pages:
                text += page.extract_text() if hasattr(page, 'extract_text') else ""
            return text
    elif extension == '.docx':
        doc = Document(filepath)
        return " ".join(paragraph.text for paragraph in doc.paragraphs)
    elif extension == '.json':
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        raise ValueError("Unsupported file type")

def get_ai_response(prompt, context):
    client = Client()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant. Use this context to answer questions: {context}"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content