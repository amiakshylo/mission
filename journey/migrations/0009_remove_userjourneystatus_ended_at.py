# Generated by Django 5.0.9 on 2024-09-20 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journey', '0008_alter_userjourneystatus_journey'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userjourneystatus',
            name='ended_at',
        ),
    ]
