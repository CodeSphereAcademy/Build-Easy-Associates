# Generated by Django 4.0.4 on 2022-07-17 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userPage', '0008_recemail_read_sendemail_read'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recemail',
            name='read',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='sendemail',
            name='read',
            field=models.BooleanField(default=0),
        ),
    ]