# Generated by Django 5.0 on 2024-04-13 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='activated',
            field=models.BooleanField(default=False),
        ),
    ]
