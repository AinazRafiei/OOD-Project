# Generated by Django 4.2.1 on 2023-07-19 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='id',
            field=models.AutoField(max_length=30, primary_key=True, serialize=False),
        ),
    ]