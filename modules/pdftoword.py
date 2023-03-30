from flask import Flask, request, make_response,send_file
import io
import os
import subprocess

app = Flask(__name__)

def convert_pdf_to_word(pdf_file):
    try:
        # Convert the PDF to Word
        cmd = ['pandoc', '-f', 'pdf', '-t', 'docx', '--output=output.docx', '-']
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=pdf_file.read())

        if process.returncode != 0:
            return "Error converting PDF to Word!", 500

        # Create the response object
        output = io.BytesIO(stdout)
        output.seek(0)
        return send_file(output, attachment_filename='converted_word.docx', as_attachment=True)

    except:
        return "Error converting PDF to Word!", 500