from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from profiles.models import UserProfile
from django.views.decorators.http import require_POST

from .services import  process_input_and_generate_feedback, run_queries_and_store_results

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
        response = run_queries_and_store_results(2, user_input, feature_1, feature_2)

        # Render an HTML template with the feedback included
        return render(request, 'books/feedback.html', {'input_text': user_input, 'feedback': response})
    else:
        # If the request method is not POST, render the form template
        return render(request, 'books/feedback.html')