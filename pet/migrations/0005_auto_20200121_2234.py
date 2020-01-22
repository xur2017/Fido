# Generated by Django 3.0.2 on 2020-01-22 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0004_auto_20200120_1657'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='verification',
        ),
        migrations.AddField(
            model_name='user',
            name='document',
            field=models.FileField(blank=True, upload_to='documents/'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photos/'),
        ),
    ]
