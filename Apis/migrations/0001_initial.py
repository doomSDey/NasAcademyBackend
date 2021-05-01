# Generated by Django 3.2 on 2021-05-01 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RateCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=200)),
                ('count', models.IntegerField(default=0)),
                ('date_time', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Slots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slots', models.CharField(max_length=200)),
                ('car', models.CharField(max_length=200)),
            ],
        ),
    ]
