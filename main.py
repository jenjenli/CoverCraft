import pandas as pd
import requests
import json

url = "https://api.arliai.com/v1/chat/completions"

ARLIA_API_KEY = "13f9f761-947d-49f7-9168-0dad486ea11f"

def load_data():
    try:
        df = pd.read_csv('cover_letter_data.csv')
        return df
    except FileNotFoundError:
        print("The dataset 'cover_letter_data.csv' does not exist.")
        return None

def generate_ai_letter(name, job_title, company, skills, experience):
    prompt = f"""
    Pretend you are {name} and write a professional cover letter applying for the {job_title} position at {company}.
    The letter should highlight the candidate's skills in {', '.join(skills)} and their relevant experience in {experience}.
    The tone should be formal, professional, and focus on how the candidate is well-suited for the position at {company}.
    """

    payload = json.dumps({
        "model": "Mistral-Nemo-12B-Instruct-2407",  # Adjust model if necessary
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "repetition_penalty": 1.1,
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "max_tokens": 1024,
        "stream": False
    })

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {ARLIA_API_KEY}"
    }

    response = requests.post(url, headers=headers, data=payload)

    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    if response.status_code == 200:
        try:
            result = response.json()
            print(f"Full Response: {json.dumps(result, indent=2)}")  # Log the full response for debugging

            cover_letter = result.get("choices", [{}])[0].get("message", {}).get("content", "No response generated.")
            return cover_letter
        except Exception as e:
            print(f"Error parsing response: {e}")
            return None
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

dataset = load_data()
if dataset is not None:
    print(dataset.head()) 

if dataset is not None and len(dataset) > 0:
    row = dataset.iloc[0]  
    name = row['name']
    job_title = row['job_title']
    company = row['company']
    skills = row['skills'].split(',') 
    experience = row['experience']
    
    cover_letter = generate_ai_letter(name, job_title, company, skills, experience)
    if cover_letter:
        print("Generated Cover Letter:\n")
        print(cover_letter)
    else:
        print("Failed to generate cover letter.")
