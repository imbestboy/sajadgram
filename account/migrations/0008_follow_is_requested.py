# Generated by Django 3.2.9 on 2021-12-03 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_user_is_new_google_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='is_requested',
            field=models.BooleanField(default=False, verbose_name='is request to follow'),
            preserve_default=False,
        ),
    ]
