# Generated by Django 3.2.9 on 2021-11-16 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_auto_20211115_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='post created time'),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated_time',
            field=models.DateTimeField(auto_now=True, verbose_name='post updated time'),
        ),
    ]
