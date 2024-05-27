# Generated by Django 5.0.6 on 2024-05-27 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('celebritypicker_app', '0009_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='randompick',
            name='movie',
        ),
        migrations.AddField(
            model_name='randompick',
            name='overview',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='randompick',
            name='poster_path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='randompick',
            name='title',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
