# Generated by Django 5.0.9 on 2024-09-24 19:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0011_alter_userprofileimage_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileimage',
            name='user_profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_image', to='user_management.userprofile'),
        ),
    ]