# Generated by Django 4.2.3 on 2023-09-20 15:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dairyapp', '0011_alter_fatrate_dairy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dairy',
            name='members',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL, verbose_name='members'),
        ),
    ]
