from flask import Flask, render_template, request, redirect, url_for
import csv
import os
from main import generate_ai_letter 

app = Flask(__name__)

app.config['ARLIA_API_KEY'] = os.getenv('ARLIA_API_KEY')

dataset_path = 'cover_letter_data.csv'

def save_to_csv(data):
    file_exists = os.path.isfile(dataset_path)

    with open(dataset_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(['name', 'job_title', 'company', 'skills', 'experience'])

        writer.writerow([data['name'], data['job_title'], data['company'], data['skills'], data['experience']])

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/generate', methods=['POST'])
def generate():
    # Get data from form
    name = request.form['name']
    job_title = request.form['job_title']
    company = request.form['company']
    skills = request.form['skills']
    experience = request.form['experience']

    form_data = {
        'name': name,
        'job_title': job_title,
        'company': company,
        'skills': skills,
        'experience': experience
    }

    save_to_csv(form_data)
    letter = generate_ai_letter(name, job_title, company, skills, experience)
    html_response = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Generated Cover Letter</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                line-height: 1.6;
                color: #333;
            }}
            .letter {{
                border: 1px solid #ccc;
                padding: 20px;
                border-radius: 10px;
                background-color: #f9f9f9;
                max-width: 800px;
                margin: 0 auto;
            }}
            pre {{
                white-space: pre-wrap;
                word-wrap: break-word;
            }}
            a {{
                display: block;
                margin-top: 20px;
                text-align: center;
                color: #007bff;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="letter">
            <pre>{letter}</pre>
        </div>
        <a href="/">Generate Another Letter</a>
    </body>
    </html>
    """
    return html_response

if __name__ == '__main__':
    app.run(debug=True)



if __name__ == "__main__":
    app.run(debug=True)
