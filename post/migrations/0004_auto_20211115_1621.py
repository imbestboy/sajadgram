# Generated by Django 3.2.9 on 2021-11-15 16:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0003_post_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savedpost',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is saved'),
        ),
        migrations.CreateModel(
            name='LikedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='is liked')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='when user liked')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.post', verbose_name='liked post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='liked user')),
            ],
        ),
    ]
