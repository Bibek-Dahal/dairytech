# Generated by Django 4.2.3 on 2023-10-14 07:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dairyapp', '0017_alter_fatrate_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fatrate',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 14, 7, 57, 24, 320349, tzinfo=datetime.timezone.utc), verbose_name='created at'),
        ),
    ]
