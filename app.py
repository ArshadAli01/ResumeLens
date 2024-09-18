import os
import re
import numpy as np
import pandas as pd
import nltk
import spacy
from flask import Flask, request, render_template, redirect, url_for
import joblib  # Import joblib for loading models
import PyPDF2  # To extract text from PDF
from werkzeug.utils import secure_filename
import warnings
from sklearn.exceptions import InconsistentVersionWarning

warnings.filterwarnings("ignore", category=InconsistentVersionWarning)


# Initialize Flask app
app = Flask(__name__)

# Configuration for file upload
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'pdf', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load models and resources using joblib
model = joblib.load('my_model.pkl')
vectorizer = joblib.load('my_vectorizer.pkl')
label_encoder = joblib.load('my_label_encoder.pkl')
global_skill_dict = joblib.load('global_skill_dict.pkl')

# Load Spacy model
nlp = spacy.load('en_core_web_sm')

# Ensure nltk stopwords are downloaded
nltk.download('stopwords')

# Function to clean the resume text
def clean_resume(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
    text = url_pattern.sub('', text)
    text = email_pattern.sub('', text)
    text = re.sub(r'[^\w\s]', '', text)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    text = ' '.join(word for word in text.split() if word.lower() not in stop_words)
    return text

# Function to get global skills based on predicted category
def get_global_skills(predicted_label):
    category = label_encoder.inverse_transform([predicted_label])[0]
    return global_skill_dict.get(category, [])

# Function to extract skills from resume text
def extract_skills(resume_text):
    nlp_text = nlp(resume_text)
    tokens = [token.text for token in nlp_text]
    all_skills = set([skill.lower() for skills in global_skill_dict.values() for skill in skills])
    extracted_skills = set(token.title() for token in tokens if token.lower() in all_skills)
    return list(extracted_skills)

# Function to check if the uploaded file is allowed (PDF or TXT)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    pdf_text = ''
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in range(len(reader.pages)):
            pdf_text += reader.pages[page].extract_text()
    return pdf_text

# Function to handle file upload and extract text
def process_uploaded_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        if filename.endswith('.txt'):
            with open(file_path, 'r') as f:
                resume_text = f.read()
        elif filename.endswith('.pdf'):
            resume_text = extract_text_from_pdf(file_path)
        else:
            resume_text = ''
        
        return resume_text
    return None

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file is uploaded
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        # Process the uploaded file and extract text
        resume_text = process_uploaded_file(file)
        if resume_text:
            cleaned_resume = clean_resume(resume_text)
            input_features = vectorizer.transform([cleaned_resume])
            predicted_label = model.predict(input_features)[0]
            predicted_category = label_encoder.inverse_transform([predicted_label])[0]

            extracted_skills = extract_skills(resume_text)
            suggested_skills = list(set(get_global_skills(predicted_label)) - set(extracted_skills))

            return render_template('index.html', 
                                   predicted_category=predicted_category, 
                                   extracted_skills=extracted_skills, 
                                   suggested_skills=suggested_skills)
    
    return render_template('index.html')

if __name__ == '__main__':
    # Ensure the uploads folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    app.run(debug=True)