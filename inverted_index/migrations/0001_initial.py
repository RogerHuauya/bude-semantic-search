# Generated by Django 5.0.2 on 2024-06-20 03:23

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track_id', models.CharField(max_length=255, unique=True)),
                ('track_name', models.CharField(max_length=255)),
                ('track_artist', models.CharField(max_length=255)),
                ('lyrics', models.TextField()),
                ('search_vector', django.contrib.postgres.search.SearchVectorField(null=True)),
            ],
            options={
                'indexes': [django.contrib.postgres.indexes.GinIndex(fields=['search_vector'], name='inverted_in_search__e01363_gin')],
            },
        ),
    ]