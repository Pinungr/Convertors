from flask import Flask, request, make_response
from PIL import Image
import io
import os
import secrets

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_image_to_pdf(file):
    if not allowed_file(file.filename):
        return 'Only PNG and JPEG files are allowed', 400
    if len(file.read()) > 10 * 1024 * 1024:
        return "Image size should be less than 10 MB!", 400

    try:
        img = Image.open(file)
    except Exception as e:
        return f'Error opening image file: {str(e)}', 400

    try:
        pdf_buffer = io.BytesIO()
        img.convert('RGB').save(pdf_buffer, format='PDF')
        pdf_buffer.seek(0)
    except Exception as e:
        return f'Error creating PDF buffer: {str(e)}', 500

    try:
        filename = secrets.token_hex(8) + '.pdf'  # generate a random filename
        response = make_response(pdf_buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    except Exception as e:
        return f'Error creating response: {str(e)}', 500

    return response