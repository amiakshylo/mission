# Generated by Django 5.0.9 on 2024-10-09 21:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principle_management', '0007_alter_rolemodel_character_name_and_more'),
        ('user_management', '0032_alter_userprinciple_user_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprinciple',
            name='principle',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='principle_management.principle'),
        ),
    ]