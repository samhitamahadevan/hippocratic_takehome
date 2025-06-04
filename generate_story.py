import json
from main import StoryGenerator

def handler(request, response):
    try:
        data = request.json()
        prompt = data.get("prompt", "")
        generator = StoryGenerator()
        story, feedback = generator.generate_story(prompt)
        # Optionally, generate PDF here if you want
        pdf_filename = generator.generate_pdf(story, feedback, prompt)
        response.body = json.dumps({
            "story": story,
            "feedback": feedback,
            "pdf_filename": pdf_filename
        })
        response.status_code = 200
    except Exception as e:
        response.body = json.dumps({"error": str(e)})
        response.status_code = 500