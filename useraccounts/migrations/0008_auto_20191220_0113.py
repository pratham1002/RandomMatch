# Generated by Django 3.0 on 2019-12-19 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccounts', '0007_auto_20191220_0101'),
    ]

    operations = [
        migrations.RenameField(
            model_name='siteuser',
            old_name='time_stamp1',
            new_name='time_stamp',
        ),
        migrations.AddField(
            model_name='siteuser',
            name='participate_request_changeTime',
            field=models.BooleanField(default=True),
        ),
    ]
