# Generated by Django 4.2.3 on 2023-10-16 03:35

import autoslug.fields
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dairyapp', '0021_alter_fatrate_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='dairy',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='bibek-dairy', editable=False, populate_from='name', unique=True, verbose_name='Slug'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fatrate',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 16, 3, 34, 48, 170426, tzinfo=datetime.timezone.utc), verbose_name='created at'),
        ),
    ]
