# Generated by Django 5.0.9 on 2024-09-12 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0011_rename_onboardinguserresponse_onboardinganswer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='onboardinganswer',
            old_name='selected_option',
            new_name='user_answer',
        ),
    ]