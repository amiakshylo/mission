# Generated by Django 5.0.6 on 2024-08-01 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category_management', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maincategory',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]