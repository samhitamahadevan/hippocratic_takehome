from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from main import StoryGenerator
import os
from datetime import datetime
import base64
from io import BytesIO

app = Flask(__name__)
CORS(app)

# Initialize the story generator
generator = StoryGenerator()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_story', methods=['POST'])
def generate_story():
    data = request.json
    user_input = data.get('prompt', '')
    
    # Generate story
    story, feedback = generator.generate_story(user_input)
    
    # Generate PDF
    pdf_filename = generator.generate_pdf(story, feedback, user_input)
    
    return jsonify({
        'story': story,
        'feedback': feedback,
        'pdf_filename': pdf_filename
    })

@app.route('/generate_image', methods=['POST'])
def generate_image():
    data = request.json
    prompt = data.get('prompt', '')
    
    try:
        # Call DALL-E API to generate image
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        
        # Get the image URL
        image_url = response['data'][0]['url']
        
        return jsonify({
            'success': True,
            'image_url': image_url
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/download_pdf/<filename>')
def download_pdf(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True) 