from pgvector.django import VectorExtension
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('audio', '0001_initial'),
    ]
    operations = [
        VectorExtension()
    ]