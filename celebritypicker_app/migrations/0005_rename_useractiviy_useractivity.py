# Generated by Django 5.0.6 on 2024-05-21 17:37

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('celebritypicker_app', '0004_useractiviy_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserActiviy',
            new_name='UserActivity',
        ),
    ]