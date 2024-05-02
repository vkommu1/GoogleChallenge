from django.urls import path

from . import views
from .views import generate_feedback, save_feedback, delete_feedback, about_me, Home

app_name = "api_interaction"

urlpatterns = [
    path("home/", Home, name="home_page"),
    path("about_me/", about_me, name="about_me"),
    path("feedback/",  generate_feedback, name="generate_feedback"),
    path("save_feedback/", save_feedback, name='save_feedback'),
    path('delete_feedback/<str:unique_id>/', delete_feedback, name='delete_feedback'),
]
