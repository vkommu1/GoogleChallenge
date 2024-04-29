import os
import google.generativeai as genai
from google.generativeai import GenerativeModel, configure
import re

def store_text(text, file_dir='media/text'):
    # Create a temporary file
    os.makedirs(file_dir, exist_ok=True)
    file_path = os.path.join(file_dir, 'input_text.txt')

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()
    
    return file_contents

def initialize_api():
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    if not GOOGLE_API_KEY:
        raise ValueError("No GOOGLE_API_KEY set. Check your .env file.")
    
    configure(api_key=GOOGLE_API_KEY)

def process_input_and_generate_feedback(user_input, feature_1, feature_2):
    """Processes the input and generates feedback."""
    initialize_api()

    # Construct the prompt with user input and features
    prompt = f"generate text description of a fake {user_input} IMPORTANT:strictly in the format [{feature_1}, {feature_2}], all lowercase"

    model = GenerativeModel(model_name="models/gemini-1.5-pro-latest")
    generated_feedback = model.generate_content(prompt)

    response = generated_feedback.text
    return response

def run_queries_and_store_results(num_queries, user_input, feature_1, feature_2):
    results = {
        feature_1: {},
        feature_2: {}
    }

    for _ in range(num_queries):
        result = process_input_and_generate_feedback(user_input, feature_1, feature_2)
        print(result)
        
        feature_str = result.strip().strip('][').split(') ')[-1]
        feature_1_value, feature_2_value = re.split(', | ', feature_str)

        results[feature_1][feature_1_value] = results[feature_1].get(feature_1_value, 0) + 1
        results[feature_2][feature_2_value] = results[feature_2].get(feature_2_value, 0) + 1

    return results
