# Generated by Django 2.2.5 on 2019-09-25 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('woofy', '0004_auto_20190925_0752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicepage',
            name='category',
            field=models.IntegerField(choices=[(1, 'hodowla'), (2, 'weterynarz'), (3, 'psi fryzjer'), (4, 'sklep zoologiczny'), (5, 'szkolenie psów'), (6, 'opieka nad psem'), (7, 'psi behawiorysta')], help_text='Wybierz jedną z kategorii', verbose_name='Kategoria'),
        ),
    ]
