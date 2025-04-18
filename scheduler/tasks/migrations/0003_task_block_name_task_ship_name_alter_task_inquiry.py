# Generated by Django 5.1.7 on 2025-04-13 13:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquiries', '0002_initial'),
        ('tasks', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='block_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='ship_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='inquiry',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inquiries.inquiry'),
        ),
    ]
