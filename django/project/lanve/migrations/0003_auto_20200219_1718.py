# Generated by Django 3.0.3 on 2020-02-19 17:18

from django.db import migrations
import lanve.models
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('lanve', '0002_auto_20200210_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lanveuser',
            name='profile_pic',
            field=stdimage.models.StdImageField(blank=True, null=True, upload_to=lanve.models.profile_pic_directory_path, verbose_name='profile picture'),
        ),
    ]