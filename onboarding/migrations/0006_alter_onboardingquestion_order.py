# Generated by Django 5.0.9 on 2024-10-04 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0005_alter_onboardingquestion_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onboardingquestion',
            name='order',
            field=models.PositiveIntegerField(null=True),
        ),
    ]