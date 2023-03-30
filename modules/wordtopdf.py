from flask import Flask, request, send_file,make_response
from docx2pdf import convert
import subprocess
import io

app = Flask(__name__)

def convert_word_to_pdf(file):
    # Check if the file is a Word document
    if not file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        return {'error': 'Please provide a Word document.'}, 400

    # Check if the file size is less than 10 MB
    if len(file.read()) > 10000000:
        return {'error': 'File size must be less than 10 MB.'}, 400
    file.seek(0)

    # Convert the Word document to PDF
    pdf_bytes = io.BytesIO()
    try:
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', '/tmp', file.filename], check=True, shell=True)
        with open(f'/tmp/{file.filename[:-5]}.pdf', 'rb') as f:
            pdf_bytes.seek(0)
            pdf_bytes.write(f.read())
    except subprocess.CalledProcessError:
        return {'error': 'Word to PDF conversion failed.'}, 500

    # Create the response object
    response = make_response(pdf_bytes.getvalue())
    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', 'attachment', filename='output.pdf')
    response.headers.set('Content-Length', str(len(pdf_bytes.getvalue())))

    return response