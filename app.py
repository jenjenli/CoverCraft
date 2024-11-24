from flask import Flask, render_template, request, redirect, url_for
import csv
import os
from main import generate_ai_letter 

app = Flask(__name__)

# Define the path to your dataset (CSV file)
dataset_path = 'cover_letter_data.csv'

# Function to save data to CSV
def save_to_csv(data):
    file_exists = os.path.isfile(dataset_path)

    # Open the CSV file and append the new data
    with open(dataset_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # If the file doesn't exist, write the header first
        if not file_exists:
            writer.writerow(['name', 'job_title', 'company', 'skills', 'experience'])

        # Write the form data
        writer.writerow([data['name'], data['job_title'], data['company'], data['skills'], data['experience']])

@app.route('/')
def index():
    return render_template('index.html')  # Ensure you have this HTML file

@app.route('/generate', methods=['POST'])
def generate():
    # Get data from form
    name = request.form['name']
    job_title = request.form['job_title']
    company = request.form['company']
    skills = request.form['skills']
    experience = request.form['experience']

    # Create a dictionary with the form data
    form_data = {
        'name': name,
        'job_title': job_title,
        'company': company,
        'skills': skills,
        'experience': experience
    }

    # Save to CSV
    save_to_csv(form_data)
    letter = generate_ai_letter(name, job_title, company, skills, experience)

    # Return the generated letter
    return f"<pre>{letter}</pre>"

    # Optionally, you could generate the cover letter here and return it as a response
    # For now, we just redirect to the index page
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)



if __name__ == "__main__":
    app.run(debug=True)
