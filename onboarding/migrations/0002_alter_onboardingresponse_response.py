# Generated by Django 5.0.6 on 2024-08-28 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onboardingresponse',
            name='response',
            field=models.IntegerField(choices=[(10, 'Strongly Agree'), (5, 'Agree'), (-5, 'Disagree'), (-10, 'Strongly Disagree')]),
        ),
    ]