# Generated by Django 5.0.9 on 2024-09-24 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0004_alter_userprofile_gender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='profile_picture',
            new_name='profile_image',
        ),
    ]
