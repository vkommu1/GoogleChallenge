from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse  # Import for potential error response

from django.db.models import Q
from profiles.models import UserProfile
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError

from .services import  process_input_and_generate_feedback, run_queries_and_store_results, get_real_world_proportions, uniform_proportions
import json
from datetime import datetime
import re
from olclient.openlibrary import OpenLibrary
from django.shortcuts import redirect
import uuid
from django.urls import reverse


def Home(request):
    return render(request, 'books/home.html')

def generate_feedback(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        feature_1 = request.POST.get('feature_1', '')
        feature_2 = request.POST.get('feature_2', '')

        # Call the service function to process the input and generate feedback
        response = run_queries_and_store_results(1, user_input, feature_1, feature_2)


        real_world_proportions = get_real_world_proportions(user_input, feature_1, feature_2)

        uniform_prop = uniform_proportions(user_input, feature_1, feature_2)
        # Render an HTML template with the feedback included
        results = {
            'uniform': uniform_prop,
            'real_world': real_world_proportions
        }
        
        results_json = json.dumps(results)

        return render(request, 'books/feedback.html', {
            'input_text': user_input,
            'feedback': response,
            'feature_1': feature_1,
            'feature_2': feature_2,
            'real_world_proportions': real_world_proportions,
            'uniform': uniform_prop,
            'results_json': results_json,
            'save_success': False       
        })
    else:
        # If the request method is not POST, render the form template
        return render(request, 'books/feedback.html')
    
@login_required
def save_feedback(request):
    print(request.POST)
    user_id = request.user.id
    profile_user = User.objects.get(pk=user_id)

    profile, created = UserProfile.objects.get_or_create(user=profile_user)

    # Ensuring the feedback_results is a list before appending
    current_feedback = profile.feedback_results if isinstance(profile.feedback_results, list) else []  

    new_input_text = request.POST.get('input_text', '')
    new_feature_1 = request.POST.get('feature_1', '')
    new_feature_2 = request.POST.get('feature_2', '')
    new_feedback = request.POST.get('feedback', '')
    new_uniform = request.POST.get('uniform')
    new_real_world_proportions = request.POST.get('real_world_proportions')

    new_feedback = {
        'input_text': new_input_text,
        'feature_1': new_feature_1,
        'feature_2': new_feature_2,
        'feedback': new_feedback,
        'uniform': new_uniform,
        'real_world_proportions': new_real_world_proportions,
        'unique_id': str(uuid.uuid4())
    }

    current_feedback.append(new_feedback)

    profile.feedback_results = current_feedback
    profile.save()

    return render(request, 'books/feedback.html', {
        'feedback': profile.feedback_results,  # Display the latest state of feedback results
        'save_success': True  # Trigger confirmation messages on the template
    })

@login_required
def delete_feedback(request, unique_id):
    if request.method == 'POST':
        profile = UserProfile.objects.get(user=request.user)
        profile.feedback_results = [feedback for feedback in profile.feedback_results if feedback.get('unique_id') != unique_id]
        profile.save()
        return redirect(reverse('profiles:user-profile', args=[request.user.id]))  # Redirect to the user profile page
    return redirect('home')  # Redirect somewhere else if not POST
