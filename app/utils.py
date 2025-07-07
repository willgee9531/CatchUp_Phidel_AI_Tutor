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

def get_ai_response(task_prompt, class_prompt, context):
    task = task_prompt
    if task_prompt == "Test Me":
        task = 'Test Me with 10 different questions. Each question should be unique and cover different aspects of the context. Provide the answers to these questions as well after the end of the last question.'
    else:
        task = task_prompt

    client = Client()
    response = client.chat.completions.create(  
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant. Use this context to answer questions always. Be consistent and whatever question asked, use this context: {context}. No preamble like saying 'Sure!' or conclusion, just answer the question."},
            {"role": "user", "content": f"Using this context: {context} i want you to {task}. My class level is {class_prompt}."}
        ],
        web_search=False
    )
    return response.choices[0].message.content