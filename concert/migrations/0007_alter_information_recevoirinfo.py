# Generated by Django 4.2.16 on 2025-06-16 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concert', '0006_alter_information_recevoirinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='information',
            name='recevoirInfo',
            field=models.CharField(max_length=25),
        ),
    ]
