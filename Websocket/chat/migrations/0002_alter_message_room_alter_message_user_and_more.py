# Generated by Django 5.0.6 on 2024-05-15 13:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message', to='chat.room'),
        ),
        migrations.AlterField(
            model_name='message',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='room',
            name='user',
        ),
        migrations.AddField(
            model_name='room',
            name='user',
            field=models.ManyToManyField(blank=True, null=True, related_name='room', to=settings.AUTH_USER_MODEL),
        ),
    ]