# Generated by Django 5.0.6 on 2024-08-28 16:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('life_sphere', '0001_initial'),
        ('user_management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='lifespherecompletion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lifesphereprogress',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='life_sphere.lifesphere'),
        ),
        migrations.AddField(
            model_name='lifesphereprogress',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.userprofile'),
        ),
    ]