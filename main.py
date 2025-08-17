from flask_cors import CORS 
from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai
import os
import fitz # PyMuPDF

app = Flask(__name__, static_folder='web')
CORS(app)

# Configure Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

@app.route('/generate', methods=['POST'])
def generate_response():
    data = request.json
    user_input = data.get('prompt', '')

    # Parse the user input
    try:
        meeting_with = user_input.split('Meeting with ')[1].split(',')[0].strip()
        agenda = user_input.split('Agenda of the meeting...')[1].strip()
    except IndexError:
        return jsonify({'error': 'Invalid input format. Please use "Meeting with [Person], Agenda of the meeting..."'}), 400

    # Read and process HDS data
    hds_data = read_hds_data(meeting_with)

    # Construct the prompt for the Gemini API
    prompt = f"""
    You are an AI assistant specialized in providing conversation tips based on personality data.
    You will be given information about a meeting and the Hogan Development Survey (HDS) data of the person you are meeting with.
    Use the provided HDS data as context to tailor your advice for a successful conversation.
    Your goal is to provide actionable tips on how to have a successful conversation, focusing on:
    1. How to start the conversation.
    2. How to build the conversation.
    3. How to explain the need (agenda) to convince the other person.

    Consider the following information:
    - Meeting with: {meeting_with}
    - Agenda: {agenda}
    - Hogan Development Survey (HDS) data of {meeting_with}: {hds_data if hds_data else "Not available."}

    Based on the HDS data and the agenda, provide specific and tailored advice.
    Also, incorporate general corporate communication best practices and grounding rules.
    Remember to maintain a professional and helpful tone.
    """

    try:
        response = model.generate_content(prompt)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def read_hds_data(person_name):
    """
    Reads and extracts relevant information from the HDS PDF file for the given person.
    This is a placeholder function and needs to be implemented based on the actual PDF structure and content.
    It should return a string containing the extracted HDS information relevant for conversation tips.
    """
    file_path = os.path.abspath(f"HOGAN_data/{person_name}_HDS.pdf")
    hds_text = ""
    if os.path.exists(file_path):
        try:
            doc = fitz.open(file_path)
            for page_num in range(doc.page_count):
                page = doc[page_num]
                hds_text += page.get_text()
            doc.close()
        except Exception as e:
            print(f"Error reading HDS file {file_path}: {e}")
            return None
    return hds_text

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('web', path)

@app.route('/')
def serve_index():
    return send_from_directory('web', 'index.html', cache_timeout=0)

if __name__ == '__main__':
 app.run(host='0.0.0.0', port=5000)
