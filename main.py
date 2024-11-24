import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import pipeline

# Initialize the tokenizer and model (you can use GPT-3 or another language model)
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")

# Use a pipeline for text generation
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Load the CSV data using pandas (instead of datasets.load_dataset)
def load_data():
    # Assuming your CSV has columns like 'name', 'job_title', 'company', 'skills', 'experience'
    try:
        df = pd.read_csv('cover_letter_data.csv')
        return df
    except FileNotFoundError:
        print("The dataset 'cover_letter_data.csv' does not exist.")
        return None

# Function to generate cover letter
def generate_ai_letter(name, job_title, company, skills, experience):
    prompt = f"""
    Write a professional cover letter for {name}, applying for the {job_title} position at {company}.
    Highlight their skills in {', '.join(skills)} and experience in {experience}.
    """

    # Generate the cover letter using the model
    response = generator(prompt, max_length=300, num_return_sequences=1)
    
    return response[0]["generated_text"]

# Example of loading the data
dataset = load_data()
if dataset is not None:
    print(dataset.head())  # Print first few rows of the dataset
