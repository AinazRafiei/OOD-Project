# Generated by Django 4.2.2 on 2023-07-23 11:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0003_rename_owner_id_channel_owner_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='published_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 23, 11, 16, 21, 62248)),
        ),
        migrations.AlterField(
            model_name='membership',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('normal', 'Normal'), ('vip', 'Vip')], default='normal', max_length=10),
        ),
    ]
