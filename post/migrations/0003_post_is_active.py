# Generated by Django 3.2.9 on 2021-11-14 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_savedpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is showable'),
        ),
    ]