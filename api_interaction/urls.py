from django.urls import path

from . import views
from reviews import views as reviewsViews
from .views import generate_feedback

app_name = "api_interaction"

urlpatterns = [
    path("", views.Home, name="home_page"),
    path("feedback/",  views.generate_feedback, name="generate_feedback"), 
]
