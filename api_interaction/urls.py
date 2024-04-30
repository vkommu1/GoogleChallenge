from django.urls import path

from . import views
from .views import generate_feedback, save_feedback, delete_feedback

app_name = "api_interaction"

urlpatterns = [
    path("home/", views.Home, name="home_page"),
    path("feedback/",  views.generate_feedback, name="generate_feedback"),
    path("save_feedback/", save_feedback, name='save_feedback'),
    path('delete_feedback/<str:unique_id>/', delete_feedback, name='delete_feedback'),
]
