from flask import Blueprint, render_template, request, jsonify
from app.utils import save_file, extract_text, get_ai_response
import os
import traceback

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    """Handles file submission and saving"""
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        
        try:
            filepath = save_file(file)
            if filepath:
                text = extract_text(filepath)
                os.remove(filepath)  # Remove the file after extracting text
                return jsonify({'success': True, 'text': text})
            else:
                return jsonify({'error': 'Invalid file type'})
        except Exception as e:
            traceback.print_exc()
            return jsonify({'error': str(e)})
        
    return render_template('index.html')

@main.route('/chat', methods=['POST'])
def chat():
    """Handles ai interaction with users chat and context"""
    data = request.json
    question = data.get('question')
    context = data.get('context')
    
    if not question or not context:
        return jsonify({'error': 'Missing question or context'})
    
    try:
        response = get_ai_response(question, context)
        return jsonify({'response': response})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)})