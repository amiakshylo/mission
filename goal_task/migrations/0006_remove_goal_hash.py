# Generated by Django 5.0 on 2024-11-15 04:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goal_task', '0005_remove_goal_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goal',
            name='hash',
        ),
    ]