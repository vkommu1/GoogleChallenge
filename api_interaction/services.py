import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings  # Import Django settings module
import google.generativeai as genai
from google.generativeai import GenerativeModel, configure
import requests
import re


def store_text(text, file_dir='media/text'):
    # Create a temporary file
    os.makedirs(file_dir, exist_ok=True)

    # Define the file path
    file_path=os.path.join(file_dir, 'input_text.txt')

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents=file.read()
    return file_contents

def initialize_api():
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    if not GOOGLE_API_KEY:
        raise ValueError("No GOOGLE_API_KEY set. Check your .env file.")
    
    configure(api_key=GOOGLE_API_KEY)


def process_input_and_generate_feedback(input_file):
    """ Processes the audio file and returns generated feedback """
    file_contents = store_text(input_file)

    initialize_api()

    prompt = "generate text description of a fake human person IMPORTANT:strictly in the format [race, gender], all lowercase"
    model = GenerativeModel(model_name="models/gemini-1.5-pro-latest")

    
    generated_feedback = model.generate_content([prompt, file_contents])

    response = generated_feedback.text

    return response

def run_queries_and_store_results(num_queries, input_file):

    results = {
        'race': {},
        'gender': {}
    }

    # Run the process_input_and_generate_feedback function
    for _ in range(num_queries):
        result = process_input_and_generate_feedback(input_file)
        print(result)
        # Extract race and gender from the result
        race_gender_str = result.strip().strip('][').split(') ')[-1]
        race, gender = re.split(', | ', race_gender_str)
        
        # Update the count for race and gender
        results['race'][race] = results['race'].get(race, 0) + 1
        results['gender'][gender] = results['gender'].get(gender, 0) + 1

    return results 



