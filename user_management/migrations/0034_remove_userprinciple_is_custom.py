# Generated by Django 5.0.9 on 2024-10-09 22:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0033_alter_userprinciple_principle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprinciple',
            name='is_custom',
        ),
    ]
