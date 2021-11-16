# Generated by Django 3.2.9 on 2021-11-16 08:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20211107_0933'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='is followed')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='follow time')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to=settings.AUTH_USER_MODEL, verbose_name='from user')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to=settings.AUTH_USER_MODEL, verbose_name='to user')),
            ],
        ),
    ]