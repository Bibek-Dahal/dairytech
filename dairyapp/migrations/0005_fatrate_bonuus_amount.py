# Generated by Django 4.2.3 on 2023-09-11 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dairyapp', '0004_delete_location_alter_milkrecord_dairy_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fatrate',
            name='bonuus_amount',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Bonous amount'),
        ),
    ]
