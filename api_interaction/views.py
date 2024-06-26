from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse  # Import for potential error response

from profiles.models import UserProfile


from .services import  process_input_and_generate_feedback, run_queries_and_store_results, get_real_world_proportions, uniform_proportions, run_gpt_queries_and_store_results, get_gpt_real_world_proportions, uniform_gpt_proportions 
import json
import re
from olclient.openlibrary import OpenLibrary
import uuid
from django.urls import reverse
import requests


def Home(request):
    return render(request, 'pages/home.html')

def about_me(request):
    return render(request, 'pages/about_me.html')


def compare_results(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        feature_1 = request.POST.get('feature_1', '')
        feature_2 = request.POST.get('feature_2', '')

        # Send input to both GPT and Gemini endpoints
        gpt_feedback = run_gpt_queries_and_store_results(5, user_input, feature_1, feature_2)
        gpt_real_world_proportions = get_gpt_real_world_proportions(user_input, feature_1, feature_2)
        gpt_uniform_prop = uniform_gpt_proportions(user_input, feature_1, feature_2)

        # Data for feedback charts
        gpt_feature_1_feedback = gpt_feedback.get(feature_1, {})
        gpt_feature_1_labels = list(gpt_feature_1_feedback.keys())
        gpt_feature_1_label = json.dumps(gpt_feature_1_labels) 
        gpt_feature_1_data = list(gpt_feature_1_feedback.values())
        gpt_feature_1_datas = json.dumps(gpt_feature_1_data)

        gpt_feature_2_feedback = gpt_feedback.get(feature_2, {})
        gpt_feature_2_labels = list(gpt_feature_2_feedback.keys())
        gpt_feature_2_label = json.dumps(gpt_feature_2_labels) 
        gpt_feature_2_data = list(gpt_feature_2_feedback.values())
        gpt_feature_2_datas = json.dumps(gpt_feature_2_data)


        # Data for real-world proportions charts, assuming values are already percentages
        gpt_real_world_feature_1 = gpt_real_world_proportions.get(feature_1 + ' Proportions', {})
        gpt_real_world_feature_1_labels = list(gpt_real_world_feature_1.keys()) + ['Other']
        gpt_real_world_feature_1_label = json.dumps(gpt_real_world_feature_1_labels)
        gpt_real_world_feature_1_data = list(gpt_real_world_feature_1.values()) + [100 - sum(gpt_real_world_feature_1.values())]
        gpt_real_world_feature_1_datas = json.dumps(gpt_real_world_feature_1_data)
        

        gpt_real_world_feature_2 = gpt_real_world_proportions.get(feature_2 + ' Proportions', {})
        gpt_real_world_feature_2_labels = list(gpt_real_world_feature_2.keys()) + ['Other']
        gpt_real_world_feature_2_label = json.dumps(gpt_real_world_feature_2_labels)
        gpt_real_world_feature_2_data = list(gpt_real_world_feature_2.values()) + [100 - sum(gpt_real_world_feature_2.values())]
        gpt_real_world_feature_2_datas = json.dumps(gpt_real_world_feature_2_data)

        gpt_results = {
            'uniform': gpt_uniform_prop,
            'real_world': gpt_real_world_proportions
        }

        gpt_results_json = json.dumps(gpt_results)

        gpt_model_name="GPT"

        gpt_return = {
            'input_text': user_input,
            'model_name': gpt_model_name,
            'results_json': gpt_results_json,
            'feedback': gpt_feedback,
            'feature_1': feature_1,
            'feature_2': feature_2,
            'real_world_proportions': gpt_real_world_proportions,
            'uniform': gpt_uniform_prop,
            'feature_1_labels': gpt_feature_1_label,
            'feature_1_data': gpt_feature_1_datas,
            'feature_2_labels': gpt_feature_2_label,
            'feature_2_data': gpt_feature_2_datas,
            'real_world_feature_1_labels': gpt_real_world_feature_1_label,
            'real_world_feature_1_data': gpt_real_world_feature_1_datas,
            'real_world_feature_2_labels': gpt_real_world_feature_2_label,
            'real_world_feature_2_data': gpt_real_world_feature_2_datas,
        }




        user_input = request.POST.get('user_input', '')
        feature_1 = request.POST.get('feature_1', '')
        feature_2 = request.POST.get('feature_2', '')

        # Send input to both GPT and Gemini endpoints
        gemini_feedback = run_queries_and_store_results(50, user_input, feature_1, feature_2)
        gemini_real_world_proportions = get_real_world_proportions(user_input, feature_1, feature_2)
        gemini_uniform_prop = uniform_proportions(user_input, feature_1, feature_2)

        # Data for feedback charts
        gemini_feature_1_feedback = gemini_feedback.get(feature_1, {})
        gemini_feature_1_labels = list(gemini_feature_1_feedback.keys())
        gemini_feature_1_label = json.dumps(gemini_feature_1_labels) 
        gemini_feature_1_data = list(gemini_feature_1_feedback.values())
        gemini_feature_1_datas = json.dumps(gemini_feature_1_data)

        gemini_feature_2_feedback = gemini_feedback.get(feature_2, {})
        gemini_feature_2_labels = list(gemini_feature_2_feedback.keys())
        gemini_feature_2_label = json.dumps(gemini_feature_2_labels) 
        gemini_feature_2_data = list(gemini_feature_2_feedback.values())
        gemini_feature_2_datas = json.dumps(gemini_feature_2_data)


        # Data for real-world proportions charts, assuming values are already percentages
        gemini_real_world_feature_1 = gemini_real_world_proportions.get(feature_1 + ' Proportions', {})
        gemini_real_world_feature_1_labels = list(gemini_real_world_feature_1.keys()) + ['Other']
        gemini_real_world_feature_1_label = json.dumps(gemini_real_world_feature_1_labels)
        gemini_real_world_feature_1_data = list(gemini_real_world_feature_1.values()) + [100 - sum(gemini_real_world_feature_1.values())]
        gemini_real_world_feature_1_datas = json.dumps(gemini_real_world_feature_1_data)
        

        gemini_real_world_feature_2 = gemini_real_world_proportions.get(feature_2 + ' Proportions', {})
        gemini_real_world_feature_2_labels = list(gemini_real_world_feature_2.keys()) + ['Other']
        gemini_real_world_feature_2_label = json.dumps(gemini_real_world_feature_2_labels)
        gemini_real_world_feature_2_data = list(gemini_real_world_feature_2.values()) + [100 - sum(gemini_real_world_feature_2.values())]
        gemini_real_world_feature_2_datas = json.dumps(gemini_real_world_feature_2_data)

        gemini_results = {
            'uniform': gemini_uniform_prop,
            'real_world': gemini_real_world_proportions
        }

        gemini_results_json = json.dumps(gemini_results)

        gemini_model_name="Gemini"

        gemini_return = {
            'input_text': user_input,
            'model_name': gemini_model_name,
            'results_json': gemini_results_json,
            'feedback': gemini_feedback,
            'feature_1': feature_1,
            'feature_2': feature_2,
            'real_world_proportions': gemini_real_world_proportions,
            'uniform': gemini_uniform_prop,
            'feature_1_labels': gemini_feature_1_label,
            'feature_1_data': gemini_feature_1_datas,
            'feature_2_labels': gemini_feature_2_label,
            'feature_2_data': gemini_feature_2_datas,
            'real_world_feature_1_labels': gemini_real_world_feature_1_label,
            'real_world_feature_1_data': gemini_real_world_feature_1_datas,
            'real_world_feature_2_labels': gemini_real_world_feature_2_label,
            'real_world_feature_2_data': gemini_real_world_feature_2_datas,
        }


        return render(request, 'pages/both_chat_page.html', {
            'gpt_feedback': gpt_return,
            'gemini_feedback': gemini_return,
            'input_text': user_input,
            'feature_1': feature_1,
            'feature_2': feature_2,
        })
    else:
        # Handle GET request or other cases
        return render(request, 'pages/both_chat_page.html')


def generate_feedback(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        feature_1 = request.POST.get('feature_1', '')
        feature_2 = request.POST.get('feature_2', '')

        feedback = run_queries_and_store_results(60, user_input, feature_1, feature_2)
        real_world_proportions = get_real_world_proportions(user_input, feature_1, feature_2)
        uniform_prop = uniform_proportions(user_input, feature_1, feature_2)

        # Data for feedback charts
        feature_1_feedback = feedback.get(feature_1, {})
        feature_1_labels = list(feature_1_feedback.keys())
        feature_1_label = json.dumps(feature_1_labels) 
        feature_1_data = list(feature_1_feedback.values())
        feature_1_datas = json.dumps(feature_1_data)

        feature_2_feedback = feedback.get(feature_2, {})
        feature_2_labels = list(feature_2_feedback.keys())
        feature_2_label = json.dumps(feature_2_labels) 
        feature_2_data = list(feature_2_feedback.values())
        feature_2_datas = json.dumps(feature_2_data)


        # Data for real-world proportions charts, assuming values are already percentages
        real_world_feature_1 = real_world_proportions.get(feature_1 + ' Proportions', {})
        real_world_feature_1_labels = list(real_world_feature_1.keys()) + ['Other']
        real_world_feature_1_label = json.dumps(real_world_feature_1_labels)
        real_world_feature_1_data = list(real_world_feature_1.values()) + [100 - sum(real_world_feature_1.values())]
        real_world_feature_1_datas = json.dumps(real_world_feature_1_data)
        

        real_world_feature_2 = real_world_proportions.get(feature_2 + ' Proportions', {})
        real_world_feature_2_labels = list(real_world_feature_2.keys()) + ['Other']
        real_world_feature_2_label = json.dumps(real_world_feature_2_labels)
        real_world_feature_2_data = list(real_world_feature_2.values()) + [100 - sum(real_world_feature_2.values())]
        real_world_feature_2_datas = json.dumps(real_world_feature_2_data)

        results = {
            'uniform': uniform_prop,
            'real_world': real_world_proportions
        }

        results_json = json.dumps(results)

        model_name="Gemini"


        return render(request, 'pages/feedback.html', {
            'input_text': user_input,
            'model_name': model_name,
            'results_json': results_json,
            'feedback': feedback,
            'feature_1': feature_1,
            'feature_2': feature_2,
            'real_world_proportions': real_world_proportions,
            'uniform': uniform_prop,
            'feature_1_labels': feature_1_label,
            'feature_1_data': feature_1_datas,
            'feature_2_labels': feature_2_label,
            'feature_2_data': feature_2_datas,
            'real_world_feature_1_labels': real_world_feature_1_label,
            'real_world_feature_1_data': real_world_feature_1_datas,
            'real_world_feature_2_labels': real_world_feature_2_label,
            'real_world_feature_2_data': real_world_feature_2_datas,
        })
    else:
        return render(request, 'pages/feedback.html')
    

def chat_page(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        feature_1 = request.POST.get('feature_1', '')
        feature_2 = request.POST.get('feature_2', '')

        feedback = run_gpt_queries_and_store_results(1, user_input, feature_1, feature_2)
        real_world_proportions = get_gpt_real_world_proportions(user_input, feature_1, feature_2)
        uniform = uniform_gpt_proportions(user_input, feature_1, feature_2)

        # Data for feedback charts
        feature_1_feedback = feedback.get(feature_1, {})
        feature_1_labels = list(feature_1_feedback.keys())
        feature_1_label = json.dumps(feature_1_labels) 
        feature_1_data = list(feature_1_feedback.values())
        feature_1_datas = json.dumps(feature_1_data)

        feature_2_feedback = feedback.get(feature_2, {})
        feature_2_labels = list(feature_2_feedback.keys())
        feature_2_label = json.dumps(feature_2_labels) 
        feature_2_data = list(feature_2_feedback.values())
        feature_2_datas = json.dumps(feature_2_data)


        # Data for real-world proportions charts, assuming values are already percentages
        real_world_feature_1 = real_world_proportions.get(feature_1 + ' Proportions', {})
        real_world_feature_1_labels = list(real_world_feature_1.keys()) + ['Other']
        real_world_feature_1_label = json.dumps(real_world_feature_1_labels)
        real_world_feature_1_data = list(real_world_feature_1.values()) + [100 - sum(real_world_feature_1.values())]
        real_world_feature_1_datas = json.dumps(real_world_feature_1_data)
        

        real_world_feature_2 = real_world_proportions.get(feature_2 + ' Proportions', {})
        real_world_feature_2_labels = list(real_world_feature_2.keys()) + ['Other']
        real_world_feature_2_label = json.dumps(real_world_feature_2_labels)
        real_world_feature_2_data = list(real_world_feature_2.values()) + [100 - sum(real_world_feature_2.values())]
        real_world_feature_2_datas = json.dumps(real_world_feature_2_data)

        results = {
            'uniform': uniform,
            'real_world': real_world_proportions
        }

        results_json = json.dumps(results)

        model_name = "GPT"


        return render(request, 'pages/chat_page.html', {
            'input_text': user_input,
            'model_name': model_name,
            'results_json': results_json,
            'feedback': feedback,
            'feature_1': feature_1,
            'feature_2': feature_2,
            'real_world_proportions': real_world_proportions,
            'uniform': uniform,
            'feature_1_labels': feature_1_label,
            'feature_1_data': feature_1_datas,
            'feature_2_labels': feature_2_label,
            'feature_2_data': feature_2_datas,
            'real_world_feature_1_labels': real_world_feature_1_label,
            'real_world_feature_1_data': real_world_feature_1_datas,
            'real_world_feature_2_labels': real_world_feature_2_label,
            'real_world_feature_2_data': real_world_feature_2_datas,
        })
    else:
        return render(request, 'pages/chat_page.html')
    
@login_required
def save_feedback(request):
    user_id = request.user.id
    profile_user = User.objects.get(pk=user_id)

    profile, created = UserProfile.objects.get_or_create(user=profile_user)

    # Ensuring the feedback_results is a list before appending
    current_feedback = profile.feedback_results if isinstance(profile.feedback_results, list) else [] 

    
    new_input_text = request.POST.get('input_text')
    model_name = request.POST.get('model_name')
    new_feature_1 = request.POST.get('feature_1')
    new_feature_2 = request.POST.get('feature_2')

    new_feedback_str = request.POST.get('feedback', '{}')
    new_feedback_str_fixed = new_feedback_str.replace("'", '"')
    new_feedback = json.loads(new_feedback_str_fixed)

    new_uniform_str = request.POST.get('uniform')
    new_uniform_str_fixed = new_uniform_str.replace("'", '"')
    new_uniform = json.loads(new_uniform_str_fixed)

    new_real_world_proportions_str = request.POST.get('real_world_proportions', '{}')
    new_real_world_proportions_str_fixed = new_real_world_proportions_str.replace("'", '"')
    new_real_world_proportions = json.loads(new_real_world_proportions_str_fixed)



    # Data for feedback charts
    feature_1_feedback = new_feedback.get(new_feature_1, {})
    feature_1_labels = list(feature_1_feedback.keys())
    feature_1_label = json.dumps(feature_1_labels) 
    feature_1_data = list(feature_1_feedback.values())
    feature_1_datas = json.dumps(feature_1_data)

    feature_2_feedback = new_feedback.get(new_feature_2, {})
    feature_2_labels = list(feature_2_feedback.keys())
    feature_2_label = json.dumps(feature_2_labels) 
    feature_2_data = list(feature_2_feedback.values())
    feature_2_datas = json.dumps(feature_2_data)


    # Data for real-world proportions charts, assuming values are already percentages
    real_world_feature_1 = new_real_world_proportions.get(new_feature_1 + ' Proportions', {})
    real_world_feature_1_labels = list(real_world_feature_1.keys()) + ['Other']
    real_world_feature_1_label = json.dumps(real_world_feature_1_labels)
    real_world_feature_1_data = list(real_world_feature_1.values()) + [100 - sum(real_world_feature_1.values())]
    real_world_feature_1_datas = json.dumps(real_world_feature_1_data)
    

    real_world_feature_2 = new_real_world_proportions.get(new_feature_2 + ' Proportions', {})
    real_world_feature_2_labels = list(real_world_feature_2.keys()) + ['Other']
    real_world_feature_2_label = json.dumps(real_world_feature_2_labels)
    real_world_feature_2_data = list(real_world_feature_2.values()) + [100 - sum(real_world_feature_2.values())]
    real_world_feature_2_datas = json.dumps(real_world_feature_2_data)



    new_feedback_entry = {
        'input_text': new_input_text,
        'feature_1': new_feature_1,
        'feature_2': new_feature_2,
        'feedback': new_feedback,
        'model_name': model_name,
        'uniform': new_uniform,
        'real_world_proportions': new_real_world_proportions,
        'feature_1_labels': feature_1_label,
        'feature_1_data': feature_1_data,
        'feature_2_labels': feature_2_label,
        'feature_2_data': feature_2_data,
        'real_world_feature_1_labels': real_world_feature_1_label,
        'real_world_feature_1_data': real_world_feature_1_data,
        'real_world_feature_2_labels': real_world_feature_2_label,
        'real_world_feature_2_data': real_world_feature_2_data,
        'unique_id': str(uuid.uuid4()).replace('-', '')
    }

    current_feedback.append(new_feedback_entry)
    profile.feedback_results = current_feedback
    profile.save()

    return render(request, 'pages/feedback.html', {
        'feedback': profile.feedback_results,
        'save_success': True
    })


@login_required
def save_both_feedback(request):
    user_id = request.user.id
    profile_user = User.objects.get(pk=user_id)

    profile, created = UserProfile.objects.get_or_create(user=profile_user)

    # Ensuring the feedback_results is a list before appending
    current_feedback = profile.feedback_results if isinstance(profile.feedback_results, list) else [] 

    
    new_input_text = request.POST.get('input_text')
    model_name = request.POST.get('model_name')
    new_feature_1 = request.POST.get('feature_1')
    new_feature_2 = request.POST.get('feature_2')

    new_feedback_str = request.POST.get('feedback', '{}')
    new_feedback_str_fixed = new_feedback_str.replace("'", '"')
    new_feedback = json.loads(new_feedback_str_fixed)

    new_uniform_str = request.POST.get('uniform')
    new_uniform_str_fixed = new_uniform_str.replace("'", '"')
    new_uniform = json.loads(new_uniform_str_fixed)

    new_real_world_proportions_str = request.POST.get('real_world_proportions', '{}')
    new_real_world_proportions_str_fixed = new_real_world_proportions_str.replace("'", '"')
    new_real_world_proportions = json.loads(new_real_world_proportions_str_fixed)



    # Data for feedback charts
    feature_1_feedback = new_feedback.get(new_feature_1, {})
    feature_1_labels = list(feature_1_feedback.keys())
    feature_1_label = json.dumps(feature_1_labels) 
    feature_1_data = list(feature_1_feedback.values())
    feature_1_datas = json.dumps(feature_1_data)

    feature_2_feedback = new_feedback.get(new_feature_2, {})
    feature_2_labels = list(feature_2_feedback.keys())
    feature_2_label = json.dumps(feature_2_labels) 
    feature_2_data = list(feature_2_feedback.values())
    feature_2_datas = json.dumps(feature_2_data)


    # Data for real-world proportions charts, assuming values are already percentages
    real_world_feature_1 = new_real_world_proportions.get(new_feature_1 + ' Proportions', {})
    real_world_feature_1_labels = list(real_world_feature_1.keys()) + ['Other']
    real_world_feature_1_label = json.dumps(real_world_feature_1_labels)
    real_world_feature_1_data = list(real_world_feature_1.values()) + [100 - sum(real_world_feature_1.values())]
    real_world_feature_1_datas = json.dumps(real_world_feature_1_data)
    

    real_world_feature_2 = new_real_world_proportions.get(new_feature_2 + ' Proportions', {})
    real_world_feature_2_labels = list(real_world_feature_2.keys()) + ['Other']
    real_world_feature_2_label = json.dumps(real_world_feature_2_labels)
    real_world_feature_2_data = list(real_world_feature_2.values()) + [100 - sum(real_world_feature_2.values())]
    real_world_feature_2_datas = json.dumps(real_world_feature_2_data)



    new_feedback_entry = {
        'input_text': new_input_text,
        'feature_1': new_feature_1,
        'feature_2': new_feature_2,
        'feedback': new_feedback,
        'model_name': model_name,
        'uniform': new_uniform,
        'real_world_proportions': new_real_world_proportions,
        'feature_1_labels': feature_1_label,
        'feature_1_data': feature_1_data,
        'feature_2_labels': feature_2_label,
        'feature_2_data': feature_2_data,
        'real_world_feature_1_labels': real_world_feature_1_label,
        'real_world_feature_1_data': real_world_feature_1_data,
        'real_world_feature_2_labels': real_world_feature_2_label,
        'real_world_feature_2_data': real_world_feature_2_data,
        'unique_id': str(uuid.uuid4()).replace('-', '')
    }

    current_feedback.append(new_feedback_entry)
    profile.feedback_results = current_feedback
    profile.save()

    return render(request, 'pages/both_chat_page.html', {
        'feedback': profile.feedback_results,
        'save_success': True
    })
    


@login_required
def save_gpt_feedback(request):
    user_id = request.user.id
    profile_user = User.objects.get(pk=user_id)

    profile, created = UserProfile.objects.get_or_create(user=profile_user)

    # Ensuring the feedback_results is a list before appending
    current_feedback = profile.feedback_results if isinstance(profile.feedback_results, list) else [] 

    model_name = request.POST.get('model_name')
    new_input_text = request.POST.get('input_text')
    new_feature_1 = request.POST.get('feature_1')
    new_feature_2 = request.POST.get('feature_2')

    new_feedback_str = request.POST.get('feedback', '{}')
    new_feedback_str_fixed = new_feedback_str.replace("'", '"')
    new_feedback = json.loads(new_feedback_str_fixed)

    new_uniform_str = request.POST.get('uniform')
    new_uniform_str_fixed = new_uniform_str.replace("'", '"')
    new_uniform = json.loads(new_uniform_str_fixed)

    new_real_world_proportions_str = request.POST.get('real_world_proportions', '{}')
    new_real_world_proportions_str_fixed = new_real_world_proportions_str.replace("'", '"')
    new_real_world_proportions = json.loads(new_real_world_proportions_str_fixed)



    # Data for feedback charts
    feature_1_feedback = new_feedback.get(new_feature_1, {})
    feature_1_labels = list(feature_1_feedback.keys())
    feature_1_label = json.dumps(feature_1_labels) 
    feature_1_data = list(feature_1_feedback.values())
    feature_1_datas = json.dumps(feature_1_data)

    feature_2_feedback = new_feedback.get(new_feature_2, {})
    feature_2_labels = list(feature_2_feedback.keys())
    feature_2_label = json.dumps(feature_2_labels) 
    feature_2_data = list(feature_2_feedback.values())
    feature_2_datas = json.dumps(feature_2_data)


    # Data for real-world proportions charts, assuming values are already percentages
    real_world_feature_1 = new_real_world_proportions.get(new_feature_1 + ' Proportions', {})
    real_world_feature_1_labels = list(real_world_feature_1.keys()) + ['Other']
    real_world_feature_1_label = json.dumps(real_world_feature_1_labels)
    real_world_feature_1_data = list(real_world_feature_1.values()) + [100 - sum(real_world_feature_1.values())]
    real_world_feature_1_datas = json.dumps(real_world_feature_1_data)
    

    real_world_feature_2 = new_real_world_proportions.get(new_feature_2 + ' Proportions', {})
    real_world_feature_2_labels = list(real_world_feature_2.keys()) + ['Other']
    real_world_feature_2_label = json.dumps(real_world_feature_2_labels)
    real_world_feature_2_data = list(real_world_feature_2.values()) + [100 - sum(real_world_feature_2.values())]
    real_world_feature_2_datas = json.dumps(real_world_feature_2_data)




    new_feedback_entry = {
        'input_text': new_input_text,
        'feature_1': new_feature_1,
        'feature_2': new_feature_2,
        'feedback': new_feedback,
        'uniform': new_uniform,
        'model_name': model_name,
        'real_world_proportions': new_real_world_proportions,
        'feature_1_labels': feature_1_label,
        'feature_1_data': feature_1_data,
        'feature_2_labels': feature_2_label,
        'feature_2_data': feature_2_data,
        'real_world_feature_1_labels': real_world_feature_1_label,
        'real_world_feature_1_data': real_world_feature_1_data,
        'real_world_feature_2_labels': real_world_feature_2_label,
        'real_world_feature_2_data': real_world_feature_2_data,
        'unique_id': str(uuid.uuid4()).replace('-', '')
    }

    current_feedback.append(new_feedback_entry)
    profile.feedback_results = current_feedback
    profile.save()

    return render(request, 'pages/both_chat_page.html', {
        'feedback': profile.feedback_results,
        'save_success': True
    })

@login_required
def delete_feedback(request, unique_id):
    if request.method == 'POST':
        profile = UserProfile.objects.get(user=request.user)
        profile.feedback_results = [feedback for feedback in profile.feedback_results if feedback.get('unique_id') != unique_id]
        profile.save()
        return redirect(reverse('profiles:user-profile', args=[request.user.id]))  # Redirect to the user profile page
    return redirect(reverse('profiles:user-profile', args=[request.user.id]))  

