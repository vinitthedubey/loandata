from flask import Flask, render_template, request, redirect
import os
from utils.ocr_capture import process_loan_document
from utils.validator import validate_data

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['document']
        if file and allowed_file(file.filename):
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)
            extracted_data = process_loan_document(path)
            errors = validate_data(extracted_data)
            return render_template('result.html', data=extracted_data, errors=errors)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
