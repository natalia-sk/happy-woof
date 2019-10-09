# Generated by Django 2.2.5 on 2019-09-24 20:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('woofy', '0002_auto_20190924_1206'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='Tytuł ogłoszenia')),
                ('content', models.CharField(max_length=140, verbose_name='Treść ogłoszenia')),
                ('city', models.CharField(default='Cała Polska', help_text='Podaj swoje miasto ułatwi to życie innym', max_length=64, verbose_name='Miasto')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
