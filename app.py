from flask import Flask, render_template, request
import os
from resume_parser import extract_resume_text
from model import calculate_similarity

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

# Create uploads folder if not exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'resume' not in request.files:
        return "No file uploaded"

    file = request.files['resume']
    job_desc = request.form['job_description']

    if file.filename == '':
        return "No selected file"

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Extract text
    resume_text = extract_resume_text(filepath)

    if resume_text.strip() == "":
        return "Could not read resume. Try another file."

    # Calculate score
    score = calculate_similarity(resume_text, job_desc)

    return f"<h2>Match Score: {score}%</h2>"

if __name__ == "__main__":
    app.run(debug=True)