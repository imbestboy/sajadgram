# Generated by Django 3.2.9 on 2021-11-06 20:41

import account.models
from django.db import migrations, models
import functools


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20211105_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, help_text='write your phone number like : +989127957054 or 09127957054', max_length=13, validators=[account.models.PhoneNumberValidator()], verbose_name='phone number'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(default='profile/default.jpeg', upload_to=functools.partial(account.models.save_image_path, *(), **{'is_background': False})),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'invalid': "NOTE : . or _ shouldn't at the beginning or endNOTE 2 : between _ and . should be charactersNOTE 3 : username should be 5 to 24 characters", 'unique': 'A user with that username already exists.'}, help_text='Required. 4 - 24 characters. Letters, digits and . and _ only.', max_length=25, unique=True, validators=[account.models.UsernameValidator()], verbose_name='username'),
        ),
    ]