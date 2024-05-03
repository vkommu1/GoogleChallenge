import os
import google.generativeai as genai
from google.generativeai import GenerativeModel, configure
import re
import openai


stored_results = None
stored_gpt_results = None


def initialize_api():
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    if not GOOGLE_API_KEY:
        raise ValueError("No GOOGLE_API_KEY set. Check your .env file.")
    
    configure(api_key=GOOGLE_API_KEY)
        

def process_input_and_generate_feedback(user_input, feature_1, feature_2):
    """Processes the input and generates feedback."""
    initialize_api()

    # Construct the prompt with user input and features
    prompt = f"generate text description of an imaginary {user_input} for my story, but based on real-life concepts only. IMPORTANT:strictly in the format: [{feature_1}, {feature_2}] all lowercase, and in English IMPORTANT: include comma"

    model = GenerativeModel(model_name='models/gemini-1.0-pro')
    generated_feedback = model.generate_content(prompt)

    response = generated_feedback.text

    return response

def run_queries_and_store_results(num_queries, user_input, feature_1, feature_2):
    global stored_results
    results = {
        feature_1: {},
        feature_2: {}
    }

    for _ in range(num_queries):

        try:
            result = process_input_and_generate_feedback(user_input, feature_1, feature_2)
        except Exception as e:
            print(f"An error occured: {e}")
            continue

        feature_str = result.strip().strip('][').split(') ')[-1]
        feature_values = re.split(',', feature_str)
        

        if len(feature_values) != 2:
            print("Unexpected number of values:", feature_values)
            continue
        
        feature_1_value, feature_2_value = feature_values

        results[feature_1][feature_1_value] = results[feature_1].get(feature_1_value, 0) + 1
        results[feature_2][feature_2_value] = results[feature_2].get(feature_2_value, 0) + 1

    stored_results = results
    return results

def get_real_world_proportions(user_input, feature_1, feature_2):
    global stored_results
    initialize_api()

    if stored_results is None:
        raise ValueError("No stored results available. Run queries first.")
    
    feature_1_proportions = {}
    for value in stored_results[feature_1].keys():
        prompt = f"generate real-world statistic estimate of number of {feature_1} as {value} in comparison to total number of {user_input}. IMPORTANT: return as one percentage ONLY in the format number"
        model = GenerativeModel(model_name='models/gemini-1.0-pro')
        generated_feedback = model.generate_content(prompt)
        response = generated_feedback.text.strip()

        try:
            proportion = float(response.strip('%'))
        except ValueError:
            raise ValueError(f"1)Unable to parse real-world proportion for {feature_1} as {value}")
            continue
        
        feature_1_proportions[value] = proportion

    feature_2_proportions = {}
    for value in stored_results[feature_2].keys():
        prompt = f"generate real-world statistic estimate of number of {feature_2} as {value} in comparison to total number of {user_input}. IMPORTANT: return number ONLY representing a percentage"
        model = GenerativeModel(model_name='models/gemini-1.0-pro')
        generated_feedback = model.generate_content(prompt)
        response = generated_feedback.text.strip()

        try:
            proportion = float(response.strip('%'))
        except ValueError:
            raise ValueError(f"2)Unable to parse real-world proportion for {feature_2} as {value}.")
            continue

        feature_2_proportions[value] = proportion
    results = {
        f"{feature_1} Proportions": feature_1_proportions,
        f"{feature_2} Proportions": feature_2_proportions
    }
    
    return results



def initialize_gpt():
    GPT_API_KEY = os.getenv('GPT_API_KEY')
    if not GPT_API_KEY:
        raise ValueError("No GPT_API_KEY set. Check your .env file.")
    openai.api_key=GPT_API_KEY


def process_gpt_input_and_generate_feedback(user_input, feature_1, feature_2):
    """Processes the input and generates feedback."""

     # Construct the prompt with user input and features
    prompt = f"generate text description of an imaginary {user_input} for my story, but based on real-life concepts only. IMPORTANT:strictly in the format: [{feature_1}, {feature_2}] all lowercase, and in English IMPORTANT: include comma"

    message = [
        {"role": "system", "content": f"You are a gpt model providing output according to {{prompt}} Again, please follow format[{feature_1}, {feature_2}] all lowercase, and in English IMPORTANT: include comma."},
        {"role": "user", "content": f"Describe {user_input} using {feature_1} and {feature_2}."},
    ]

    response =  openai.chat.completions.create(
        model = "gpt-3.5-turbo-0125",
        messages = message
    )
    output = response.choices[0].message.content

    return output


def run_gpt_queries_and_store_results(num_queries, user_input, feature_1, feature_2):
    global stored_gpt_results
    initialize_gpt()
    results = {
        feature_1: {},
        feature_2: {}
    }

    for _ in range(num_queries):
        try:
            result = process_gpt_input_and_generate_feedback(user_input, feature_1, feature_2)
            if not result:
                continue
        except Exception as e:
            print(f"An error occured: {e}")
            continue

        feature_values = re.findall(r"[\w\s'-]+", result)
        if len(feature_values) != 2:
            print("Unexpected number of values:", feature_values)
            continue

        feature_1_value, feature_2_value =feature_values

        results[feature_1][feature_1_value] = results[feature_1].get(feature_1_value, 0) + 1
        results[feature_2][feature_2_value] = results[feature_2].get(feature_2_value, 0) + 1

    stored_gpt_results = results
    return results

def get_gpt_real_world_proportions(user_input, feature_1, feature_2):
    global stored_gpt_results
    print(stored_gpt_results)
    initialize_gpt()

    if stored_gpt_results is None:
        raise ValueError("No stored results available. Run queries first.")
    
    feature_1_proportions = {}

    for value in stored_gpt_results[feature_1].keys():
        prompt = f"generate real-world statistic estimate of number of {feature_1} as {value} in comparison to total number of {user_input} in the world. IMPORTANT: return as one percentage ONLY in the format number, no WORDS"
        message = [
        {"role": "system", "content": f"You are a gpt model providing output according to {{prompt}} Again, please follow format number ONLY (ex response: 5)"},
        {"role": "user", "content": f"generate real-world statistic estimate of number of {feature_1} as {value} in comparison to total number of {user_input} in the world. IMPORTANT: return as a single number ONLY representing percentage, no other words (ex response: 5)"},
        ]

        response =  openai.chat.completions.create(
            model = "gpt-3.5-turbo-0125",
            messages = message
        )
        proportion = float(response.choices[0].message.content.strip('%'))
        feature_1_proportions[value] = proportion
        
        
    feature_2_proportions = {}
    for value in stored_gpt_results[feature_2].keys():
        prompt = f"generate real-world statistic estimate of number of {feature_2} as {value} in comparison to total number of {user_input}. IMPORTANT: return number ONLY representing a percentage"
        message = [
        {"role": "system", "content": f"You are a gpt model providing output according to {{prompt}} Again, please follow format number ONLY (ex response: 5)"},
        {"role": "user", "content": f"generate real-world statistic estimate of number of {feature_1} as {value} in comparison to total number of {user_input} in the world. IMPORTANT: return as a single number ONLY representing percentage, no other words (ex response: 5)"},
        ]
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=message
        )
        proportion = float(response.choices[0].message.content.strip('%'))
        feature_2_proportions[value] = proportion
    
    
    results = {
        f"{feature_1} Proportions": feature_1_proportions,
        f"{feature_2} Proportions": feature_2_proportions
    }
    
    return results

def uniform_proportions(user_input, feature_1, feature_2):
    """Processes the input and generates feedback."""
    initialize_api()

    # Construct the prompt with user input and features
    
    model = GenerativeModel(model_name='models/gemini-1.0-pro')

    prompt_feature_1 = f"generate all possible popular responses of {feature_1} in {user_input}. IMPORTANT: all English"
    generated_feedback_1 = model.generate_content(prompt_feature_1)
    response_1 = generated_feedback_1.text.strip().split('\n')


    prompt_feature_2 = f"generate all possible popular responses of {feature_2} in {user_input}. IMPORTANT: all English"
    generated_feedback_2 = model.generate_content(prompt_feature_2)
    response_2 = generated_feedback_2.text.strip().split('\n')

    results = {
        feature_1: response_1, 
        feature_2: response_2,
    }

    return results

def uniform_gpt_proportions(user_input, feature_1, feature_2):
    """Processes the input and generates feedback."""
    initialize_gpt()

    # Construct the prompt with user input and features
    
    prompt_feature_1 = f"generate all possible popular responses of {feature_1} in {user_input}. Response should only be 1-2 words. IMPORTANT: all English"
    message = [
        {"role": "system", "content": f"You are a gpt model providing output according to {{prompt_feature_1}} Response should only be 1-2 words. IMPORTANT: all English, IMPORTANT:don't use ANY double quotes like \" in your response. You can use * instead."},
        {"role": "user", "content": f"generate all possible popular responses of {feature_1} in {user_input}. Response should only be 1-2 words. IMPORTANT: all English, IMPORTANT:don't use ANY double quotes like \" in your response. You can use * instead."},
    ]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=message,
        logit_bias={"1": -100, "6": -100}
    )

    response_1 = response.choices[0].message.content.strip().split('\n')

    prompt_feature_2 = f"generate all possible popular responses of {feature_2} in {user_input}. Response should only be 1-2 words. IMPORTANT: all English"
    message = [
        {"role": "system", "content": f"You are a gpt model providing output according to {{prompt_feature_2}} Response should only be 1-2 words. Again, please follow format english ONLY, don't use quotes"},
        {"role": "user", "content": f"generate all possible popular responses of {feature_2} in {user_input}. Response should only be 1-2 words. IMPORTANT: all English, don't use ANY  quotes like \" in your response. You can use * instead"},
    ]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=message,
        logit_bias={"1": -100, "6": -100}
    )

    response_2 = response.choices[0].message.content.strip().split('\n')
    results = {
        feature_1: response_1, 
        feature_2: response_2,
    }

    return results













    

    
