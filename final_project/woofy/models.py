from django.contrib.auth.models import User, Group
from django.db import models


class WoofyPost(models.Model):
    content = models.CharField(max_length=250, verbose_name='Treść', help_text='max. 250 znaków')
    # image = models.ImageField(upload_to='post_image', blank=True, null=True)
    city = models.CharField(max_length=64,
                            verbose_name='Miasto',
                            help_text='Podaj swoje miasto, ułatwi to życie innym',
                            default='Cała Polska')
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


CATEGORIES = (
    (1, "hodowla"),
    (2, "weterynarz"),
    (3, "psi fryzjer"),
    (4, "sklep zoologiczny"),
    (5, "szkolenie psów"),
    (6, "opieka nad psem"),
    (7, "psi behawiorysta")
)


class ServicePage(models.Model):
    name = models.CharField(max_length=64, verbose_name='Nazwa Twojej firmy')
    category = models.IntegerField(choices=CATEGORIES,
                                   verbose_name='Kategoria',
                                   help_text='Wybierz jedną z kategorii')
    description = models.CharField(max_length=255,
                                   verbose_name='Dodatkowy opis',
                                   help_text='max. 128 znaków',
                                   null=True)
    address = models.CharField(max_length=128, verbose_name='Adres', null=True)
    city = models.CharField(max_length=64, verbose_name='Miasto')
    phone = models.CharField(max_length=16, verbose_name='Telefon', null=True)
    email = models.EmailField(verbose_name='e-mail', null=True)
    homepage = models.URLField(verbose_name='Twoja strona www', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Announcement(models.Model):
    title = models.CharField(max_length=64, verbose_name='Tytuł ogłoszenia')
    content = models.CharField(max_length=140, verbose_name='Krótki opis',
                               help_text='Opis, który będzie widoczny na stronie głównej')
    all_details = models.TextField(verbose_name='Szczegóły')
    city = models.CharField(max_length=64,
                            verbose_name='Miasto',
                            help_text='Podaj swoje miasto, ułatwi to życie innym',
                            default='Cała Polska')
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.CharField(max_length=140, verbose_name='Komentarz')
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(WoofyPost, on_delete=models.CASCADE)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender', verbose_name='Nadawca')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver', verbose_name='Odbiorca')
    title = models.CharField(max_length=128, verbose_name='Temat')
    content = models.TextField(verbose_name='Wiadomość')
    creation_date = models.DateTimeField(auto_now_add=True)
