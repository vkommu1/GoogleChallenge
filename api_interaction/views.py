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
    print("here")
    user_id = request.user.id
    profile_user = User.objects.get(pk=user_id)

    profile, created = UserProfile.objects.get_or_create(user=profile_user)



    uniform = request.POST.get('uniform')
    real_world_proportions = request.POST.get('real_world_proportions')
    
    profile.feedback_results = {
        'uniform': uniform,
        'real_world_proportions': real_world_proportions
    }


    profile.save()
    
    return render(request, 'books/feedback.html', {
        'input_text': request.POST.get('user_input', ''),
        'feedback': profile.feedback_results,  # or any other context needed for the feedback page
        'save_success': True  # You can use this to trigger confirmation messages on the template
    })