# Generated by Django 3.2.8 on 2021-10-21 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='avatar',
            field=models.ImageField(upload_to='avatars'),
        ),
    ]
