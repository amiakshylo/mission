# Generated by Django 5.0.6 on 2024-08-01 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0004_alter_userrole_is_custom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrole',
            name='is_custom',
            field=models.BooleanField(default=False),
        ),
    ]