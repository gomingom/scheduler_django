# Generated by Django 5.1.7 on 2025-04-13 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ship_name', models.CharField(max_length=150)),
                ('block_name', models.CharField(max_length=150)),
                ('request_date', models.DateField()),
                ('is_accepted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('대기', '대기'), ('승인', '승인'), ('반려', '반려'), ('취소', '취소')], default='대기', max_length=150)),
                ('device', models.CharField(choices=[('일반측정', '일반측정'), ('3D Scanner', '3D Scanner')], max_length=150)),
                ('inquiry_detail', models.TextField()),
            ],
        ),
    ]
