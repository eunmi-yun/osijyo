# Generated by Django 3.2.16 on 2022-12-14 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('log', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='history',
            fields=[
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('reg_date', models.DateField()),
                ('disease_name', models.CharField(max_length=50)),
                ('disease_cure', models.CharField(max_length=200)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='%Y/%m/%d')),
            ],
            options={
                'db_table': 'log_log',
                'managed': False,
            },
        ),
    ]