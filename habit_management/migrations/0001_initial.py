# Generated by Django 5.0.6 on 2024-08-01 03:15

import core.models
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateTimeField(validators=[core.models.validate_start_due_date])),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('progress', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)])),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('frequency', models.JSONField(default=dict)),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category_management.subcategory')),
            ],
        ),
    ]