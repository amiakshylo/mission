# Generated by Django 5.0.9 on 2024-09-20 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journey', '0004_journey_journey_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='journeystep',
            options={'ordering': ['step_number']},
        ),
    ]
