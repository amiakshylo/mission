# Generated by Django 5.0.9 on 2024-10-09 16:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0011_alter_userresponse_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userresponse',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onboarding.onboardingquestion'),
        ),
        migrations.AlterField(
            model_name='userresponse',
            name='user_answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onboarding.answeroption'),
        ),
    ]