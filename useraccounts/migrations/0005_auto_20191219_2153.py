# Generated by Django 3.0 on 2019-12-19 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccounts', '0004_siteuser_verification_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteuser',
            name='gender',
            field=models.CharField(default='M', max_length=2),
        ),
        migrations.AddField(
            model_name='siteuser',
            name='participate_request',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='siteuser',
            name='participate_request_granted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='siteuser',
            name='verification_code',
            field=models.CharField(default='0', max_length=10),
        ),
    ]
