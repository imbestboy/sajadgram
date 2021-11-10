# Generated by Django 3.2.9 on 2021-11-07 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20211106_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.CharField(blank=True, max_length=150, verbose_name='biography'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=15, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=15, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='website',
            field=models.URLField(blank=True, max_length=30, verbose_name='website'),
        ),
    ]
