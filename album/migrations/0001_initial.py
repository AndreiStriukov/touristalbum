# Generated by Django 5.0.6 on 2024-06-15 18:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JourneyAlbum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_name', models.CharField(max_length=32)),
                ('a_slug', models.SlugField(max_length=32, unique=True)),
                ('j_month', models.PositiveSmallIntegerField(default=1)),
                ('j_year', models.PositiveSmallIntegerField(default=2024)),
                ('j_place', models.CharField(max_length=64)),
                ('person_number', models.PositiveSmallIntegerField(default=1)),
                ('a_descr', models.TextField(blank=True, null=True)),
                ('a_date_create', models.DateTimeField(auto_now_add=True)),
                ('a_date_update', models.DateTimeField(auto_now=True)),
                ('a_is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['a_name'],
            },
        ),
        migrations.CreateModel(
            name='TypeJourney',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('j_type_name', models.CharField(max_length=32)),
                ('j_type_descr', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ph_file', models.ImageField(upload_to='img')),
                ('ph_name', models.CharField(max_length=36)),
                ('ph_slug', models.SlugField(max_length=255, unique=True)),
                ('ph_descr', models.TextField(blank=True, null=True)),
                ('ph_date_create', models.DateTimeField(auto_now_add=True)),
                ('ph_date_update', models.DateTimeField(auto_now=True)),
                ('ph_is_active', models.BooleanField(default=True)),
                ('ph_album', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='album.journeyalbum')),
            ],
            options={
                'ordering': ['-ph_date_create'],
            },
        ),
        migrations.AddField(
            model_name='journeyalbum',
            name='j_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='album.typejourney'),
        ),
    ]
