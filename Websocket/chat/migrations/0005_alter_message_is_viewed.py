# Generated by Django 5.0.6 on 2024-05-17 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_message_is_viewed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='is_viewed',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]