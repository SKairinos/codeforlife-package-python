# Generated by Django 3.2.16 on 2023-01-24 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0033_password_reset_tracking_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyactivity',
            name='daily_school_student_lockout_reset',
            field=models.PositiveIntegerField(default=0),
        ),
    ]