# Generated by Django 3.0 on 2019-12-19 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccounts', '0003_auto_20191219_0040'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteuser',
            name='verification_code',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]
