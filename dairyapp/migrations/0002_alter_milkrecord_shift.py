# Generated by Django 4.2.3 on 2023-07-28 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dairyapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milkrecord',
            name='shift',
            field=models.CharField(choices=[('morning', 'morning'), ('night', 'night')], max_length=10),
        ),
    ]
