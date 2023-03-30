from flask import Flask, request, make_response, render_template, send_file
from PIL import Image
import io
from fpdf import FPDF
import os
from modules import imagetopdf
from modules import wordtopdf
from modules import pdftoword

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/imagetopdf")
def render_imagetopdf():
    return render_template("imagetopdf.html")

@app.route("/wordtopdf")
def render_wordtopdf():
    return render_template("wordtopdf.html")

@app.route("/pdftoword")
def render_pdftoword():
    return render_template("pdftoword.html")


@app.route('/api/imagetopdf', methods=['POST'])
def convert_image_to_pdf():
    if 'image' not in request.files:
        return "No image selected!", 400
def api_imagetopdf():
    if 'image' not in request.files:
        return "No image selected!", 400
    image = request.files['image']
    if image.filename == '':
        return "No image selected!", 400
    return convert_image_to_pdf(image)

@app.route('/api/wordtopdf', methods=['POST'])
def convert_word_to_pdf():
    if 'file' not in request.files:
        return "No image selected!", 400
def wordtopdf_api():
    file = request.files['file']
    if not file:
        return {'error': 'Please provide a file.'}, 400
    return convert_word_to_pdf(file)


@app.route('/api/pdftoword', methods=['POST'])
def convert_pdf_to_word():
   def wordtopdf_api():
    file = request.files['file']
    if not file:
        return {'error': 'Please provide a file.'}, 400
    return convert_pdf_to_word(file)

if __name__ == "__main__":
    app.run(debug=True)