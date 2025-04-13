# Generated by Django 5.1.7 on 2025-04-13 13:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquiries', '0002_initial'),
        ('tasks', '0003_task_block_name_task_ship_name_alter_task_inquiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='block_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='inquiry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inquiries.inquiry'),
        ),
        migrations.AlterField(
            model_name='task',
            name='ship_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
