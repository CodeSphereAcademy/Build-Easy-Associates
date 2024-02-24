# Generated by Django 4.0 on 2024-02-24 06:18

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.CharField(max_length=50, null=True)),
                ('address', models.CharField(max_length=200)),
                ('plotSize', models.IntegerField()),
                ('builtArea', models.IntegerField()),
                ('numFloor', models.IntegerField()),
                ('plotAddress', models.CharField(max_length=200)),
                ('projectDescription', models.CharField(max_length=500, null=True)),
                ('interiorArea', models.IntegerField(default=0, null=True)),
                ('basementArea', models.IntegerField(default=0, null=True)),
                ('totalCost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('approved', models.BooleanField(default=False)),
                ('referenceID', models.CharField(default='', max_length=50, null=True)),
                ('projectTitle', models.CharField(default='', max_length=50, null=True)),
                ('tokenAmount', models.IntegerField(default=0, null=True)),
                ('pendingAmount', models.IntegerField(default=0, null=True)),
                ('clientRequirements', models.CharField(default='', max_length=500, null=True)),
                ('projectStartDate', models.DateField(default=datetime.date.today, null=True)),
                ('projectEndDate', models.DateField(default=datetime.date.today, null=True)),
                ('projectStatus', models.CharField(default='Pending', max_length=50, null=True)),
                ('projectStarted', models.CharField(default='No', max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClientServiceInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.ImageField(null=True, upload_to='')),
                ('name', models.CharField(max_length=30)),
                ('cost', models.FloatField()),
                ('details', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Service',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic1', models.ImageField(upload_to='')),
                ('pic2', models.ImageField(upload_to='')),
                ('projectTitle', models.CharField(max_length=20)),
                ('projectCost', models.IntegerField(null=True)),
                ('projectArea', models.IntegerField(null=True)),
                ('projectDesc', models.CharField(max_length=500)),
                ('publishDate', models.DateField(default=datetime.date.today, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RecEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
                ('msg', models.CharField(max_length=2000)),
                ('date', models.DateField(default=datetime.date.today, null=True)),
                ('read', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Received Email',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.ImageField(upload_to='')),
                ('name', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=15, null=True)),
                ('jobRole', models.CharField(max_length=30, null=True)),
                ('jobDesc', models.CharField(max_length=200)),
                ('salary', models.IntegerField()),
                ('joiningDate', models.DateField(default=datetime.date.today, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UpdateVariable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('YOE', models.IntegerField(default=0)),
                ('totalProjects', models.IntegerField(default=0)),
                ('totalEmployees', models.IntegerField(default=0)),
                ('totalClients', models.IntegerField(default=0)),
                ('totalPartners', models.IntegerField(default=0)),
                ('totalCities', models.IntegerField(default=0)),
                ('totalArea', models.IntegerField(default=0)),
                ('PAC', models.IntegerField(default=0)),
                ('IAC', models.IntegerField(default=0)),
                ('BAC', models.IntegerField(default=0)),
                ('BACS', models.FloatField(default=0.0)),
                ('yt1', models.CharField(default='', max_length=200, null=True)),
                ('yt2', models.CharField(default='', max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Variable',
            },
        ),
        migrations.CreateModel(
            name='WorkPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userPage.clientinfo')),
            ],
        ),
        migrations.CreateModel(
            name='SendEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('msg', models.CharField(max_length=2000)),
                ('date', models.DateField(default=datetime.date.today, null=True)),
                ('read', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userPage.clientinfo')),
            ],
            options={
                'verbose_name': 'Send Email',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic1', models.ImageField(null=True, upload_to='')),
                ('pic2', models.ImageField(null=True, upload_to='')),
                ('pic3', models.ImageField(blank=True, null=True, upload_to='')),
                ('pic4', models.ImageField(blank=True, null=True, upload_to='')),
                ('pic5', models.ImageField(blank=True, null=True, upload_to='')),
                ('pic6', models.ImageField(blank=True, null=True, upload_to='')),
                ('pic7', models.ImageField(blank=True, null=True, upload_to='')),
                ('pic8', models.ImageField(blank=True, null=True, upload_to='')),
                ('pic9', models.ImageField(blank=True, null=True, upload_to='')),
                ('pic10', models.ImageField(blank=True, null=True, upload_to='')),
                ('name', models.CharField(max_length=20, null=True)),
                ('amtPaid', models.IntegerField(null=True)),
                ('detail', models.CharField(max_length=200)),
                ('publishDate', models.DateField(default=datetime.date.today, null=True)),
                ('workPost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userPage.workpost')),
            ],
        ),
        migrations.AddField(
            model_name='clientinfo',
            name='serviceOpted',
            field=models.ManyToManyField(to='userPage.ClientServiceInfo'),
        ),
    ]
