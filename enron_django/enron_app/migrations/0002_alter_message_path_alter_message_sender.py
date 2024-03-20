# Generated by Django 5.0.2 on 2024-03-20 09:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enron_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='path',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enron_app.mailadress'),
        ),
    ]
