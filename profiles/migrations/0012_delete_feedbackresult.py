# Generated by Django 4.2.1 on 2024-04-30 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_remove_userprofile_feedback_results_feedbackresult'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FeedbackResult',
        ),
    ]
