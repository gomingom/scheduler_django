# Generated by Django 5.1.7 on 2025-04-03 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='work_time',
            field=models.CharField(max_length=10),
        ),
    ]
