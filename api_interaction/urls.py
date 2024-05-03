from django.urls import path

from . import views
from .views import save_both_feedback, compare_results, save_gpt_feedback, chat_page, generate_feedback, save_feedback, delete_feedback, about_me, Home

app_name = "api_interaction"

urlpatterns = [
    path("home/", Home, name="home_page"),
    path("about_me/", about_me, name="about_me"),
    path("feedback/",  generate_feedback, name="generate_feedback"),
    path("gpt_feedback/", chat_page, name="gpt_generate_feedback"), 
    path("save_feedback/", save_feedback, name='save_feedback'),
    path("save_gpt_feedback/", save_gpt_feedback, name='save_gpt_feedback'),
    path("save_both", save_both_feedback, name='save_both'),
    path("compare/",compare_results, name="compare_results"),
    path('delete_feedback/<str:unique_id>/', delete_feedback, name='delete_feedback'),
]
