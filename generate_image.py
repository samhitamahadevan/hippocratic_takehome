import json
from main import StoryGenerator

def handler(request, response):
    try:
        data = request.json()
        prompt = data.get("prompt", "")
        generator = StoryGenerator()
        image_filename = generator.generate_image(prompt)
        # You may want to serve the image as a URL or base64 string
        response.body = json.dumps({
            "success": bool(image_filename),
            "image_url": f"/{image_filename}" if image_filename else None
        })
        response.status_code = 200
    except Exception as e:
        response.body = json.dumps({"error": str(e)})
        response.status_code = 500