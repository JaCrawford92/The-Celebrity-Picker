# Generated by Django 5.0.6 on 2024-05-22 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('celebritypicker_app', '0005_rename_useractiviy_useractivity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivity',
            name='show',
            field=models.CharField(max_length=50),
        ),
    ]
