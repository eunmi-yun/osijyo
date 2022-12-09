# Generated by Django 4.1.1 on 2022-12-09 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='disease',
            fields=[
                ('disease_code', models.AutoField(primary_key=True, serialize=False)),
                ('disease_name', models.CharField(max_length=45)),
                ('disease_cure', models.CharField(max_length=45)),
                ('scientific_name', models.CharField(max_length=50)),
                ('disease_group', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'disease',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='history',
            fields=[
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('reg_date', models.DateField()),
                ('disease_name', models.CharField(max_length=50)),
                ('disease_cure', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'history',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_pw', models.CharField(max_length=45)),
                ('user_name', models.CharField(max_length=45)),
                ('user_email', models.CharField(max_length=50)),
                ('reg_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
    ]
