# ResumeLens

ResumeLens is a machine learning-powered tool designed to revolutionize the way recruiters analyze resumes. It automates the resume analysis process, providing recruiters with instant, detailed insights into candidates' profiles, skills, and relevant experiences.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Usage](#usage)
- [How It Works](#how-it-works)


## Features

- **Automated Resume Categorization:** Quickly categorize resumes based on predefined job roles.
- **Skill Extraction:** Extract relevant skills from resumes using natural language processing.
- **Skill Suggestions:** Suggest missing skills based on job requirements and extracted skills.
- **User-Friendly Interface:** Easy-to-use web interface for seamless interaction.
- **PDF and Text File Support:** Upload resumes in PDF or text format for analysis.

## Tech Stack

ResumeLens is built using a powerful tech stack:

- **Backend:** Python with pandas, numpy, nltk, scikit-learn, spacy, seaborn, matplotlib, for machine learning model development.
- **NLP Models:** SpaCy and BERT for named entity recognition and text summarization.
- **Frontend:** Basic HTML, CSS and JS for a user-friendly web interface.
- **Database:** PostgreSQL or MongoDB for efficient data storage.
- **Deployment:** Docker and cloud services like AWS or Azure to ensure scalability and reliability.

## **Usage**

1. On the homepage, you can upload a resume in **PDF** or **text format**.
2. Click on the **"Categorize Resume"** button to start the analysis.

The tool will display:
- The **predicted job category**.
- **Extracted skills** from the resume.
- **Suggested missing skills** based on the uploaded resume.

## **How It Works**

### 1. **Data Preprocessing**
- The uploaded resume is cleaned to remove **URLs, emails, special characters**, and **stopwords** using the `clean_resume` function.

### 2. **Feature Extraction**
- The cleaned resume text is transformed into numerical format using **TF-IDF vectorization** with `vectorizer.transform`.

### 3. **Model Prediction**
- A trained **Logistic Regression** model (`model.predict`) predicts the **job category** of the resume.

### 4. **Skill Extraction**
- Relevant skills are extracted from the resume text using the `extract_skills` function, which matches tokens with a **global skill dictionary**.

### 5. **Skill Suggestion**
- **Missing skills** are suggested by comparing the extracted skills with the **ideal skill set** for the predicted category using `get_global_skills`.

---

## This is all about ResumeLens.
## Thank You!


   
