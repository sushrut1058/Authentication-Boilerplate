# Generated by Django 5.0 on 2024-04-13 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_customuser_verified_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
