# Generated by Django 4.1 on 2022-12-13 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("log", "0005_alter_log_table"),
    ]

    operations = [
        migrations.AlterModelTable(name="log", table="log_log",),
    ]
