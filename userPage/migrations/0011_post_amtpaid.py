# Generated by Django 4.0.4 on 2022-07-19 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userPage', '0010_updatevariable_yt1_updatevariable_yt2'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='amtPaid',
            field=models.IntegerField(null=True),
        ),
    ]