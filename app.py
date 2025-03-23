import os
from flask import Flask, request, jsonify
import boto3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow all origins by default
# Initialize AWS Textract client using environment variables for security
session = boto3.Session(
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.environ.get('AWS_SESSION_TOKEN'),  # Optional if using temporary credentials
    region_name='us-west-2'
)
textract_client = session.client('textract')

def extract_text_from_image(image_bytes):
    response = textract_client.detect_document_text(Document={'Bytes': image_bytes})
    text = ''
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            text += block['Text'] + '\n'
    return text

@app.route('/extract_text', methods=['POST'])
def extract_text():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    image_bytes = image_file.read()
    extracted_text = extract_text_from_image(image_bytes)
    return jsonify({'extracted_text': extracted_text})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
