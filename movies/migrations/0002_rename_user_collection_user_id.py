# Generated by Django 5.0.7 on 2024-07-17 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collection',
            old_name='user',
            new_name='user_id',
        ),
    ]