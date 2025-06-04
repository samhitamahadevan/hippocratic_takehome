import os

def handler(request, response):
    filename = request.path_params[0]  # from /download_pdf/(.*)
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            response.body = f.read()
        response.headers["Content-Type"] = "application/pdf"
        response.status_code = 200
    else:
        response.body = b"File not found"
        response.status_code = 404