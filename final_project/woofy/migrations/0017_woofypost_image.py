# Generated by Django 2.2.5 on 2019-09-27 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('woofy', '0016_auto_20190926_2340'),
    ]

    operations = [
        migrations.AddField(
            model_name='woofypost',
            name='image',
            field=models.ImageField(blank=True, upload_to='post_image', verbose_name='Dodaj zdjęcie/obrazek'),
        ),
    ]
