# Generated by Django 5.1.1 on 2024-10-21 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0002_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2024-01-01 00:00:00'),
            preserve_default=False,
        ),
    ]