# Generated by Django 5.0.6 on 2024-05-24 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('celebritypicker_app', '0006_alter_useractivity_show'),
    ]

    operations = [
        migrations.AddField(
            model_name='actor',
            name='biography',
            field=models.CharField(blank=True),
        ),
        migrations.AddField(
            model_name='actor',
            name='profile_img_url',
            field=models.URLField(blank=True),
        ),
    ]