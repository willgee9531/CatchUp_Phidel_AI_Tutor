from flask import Blueprint, render_template, request, jsonify
from app.utils import save_file, extract_text, get_ai_response
import os
import traceback

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("Received POST request")
        if 'file' not in request.files:
            print("No file part in request")
            return jsonify({'error': 'No file part'})
        file = request.files['file']
        if file.filename == '':
            print("No selected file")
            return jsonify({'error': 'No selected file'})
        
        print(f"Processing file: {file.filename}")
        try:
            filepath = save_file(file)
            if filepath:
                print(f"File saved to: {filepath}")
                text = extract_text(filepath)
                os.remove(filepath)  # Remove the file after extracting text
                print("File processed successfully")
                return jsonify({'success': True, 'text': text})
            else:
                print("Invalid file type")
                return jsonify({'error': 'Invalid file type'})
        except Exception as e:
            print(f"Error processing file: {str(e)}")
            traceback.print_exc()
            return jsonify({'error': str(e)})
        
    return render_template('index.html')

@main.route('/chat', methods=['POST'])
def chat():
    print("Received chat request")
    data = request.json
    question = data.get('question')
    context = data.get('context')
    
    if not question or not context:
        print("Missing question or context")
        return jsonify({'error': 'Missing question or context'})
    
    try:
        print("Generating AI response")
        response = get_ai_response(question, context)
        print("AI response generated successfully")
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error generating AI response: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)})