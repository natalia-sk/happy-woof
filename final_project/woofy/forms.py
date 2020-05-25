from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField, UserChangeForm
from django.contrib.auth.models import Group


from woofy.models import MyUser, WoofyPost, Announcement, ServicePage, Comment, Message


# dodawanie nowego posta
class AddNewPostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea,
                              label='Treść',
                              help_text='max. 250 znaków')

    class Meta:
        model = WoofyPost
        fields = ['content', 'city']


# dodawanie ogłoszenia
class AddNewAnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        exclude = ['creation_date', 'user']


# dodawanie strony usługodawcy
class AddServicePageForm(forms.ModelForm):
    description = forms.CharField(max_length=128, widget=forms.Textarea, required=False, label='Opis')
    address = forms.CharField(required=False, label='Adres')
    phone = forms.CharField(required=False, label='Telefon')
    email = forms.EmailField(required=False, label='E-mail')
    homepage = forms.URLField(required=False, label='WWW')

    class Meta:
        model = ServicePage
        exclude = ['user']


# dodawanie komentarzy do postów
class CommentForm(forms.ModelForm):
    content = forms.CharField(max_length=140, widget=forms.Textarea, label='Komentarz')

    class Meta:
        model = Comment
        fields = ['content']


# wysyłanie wiadomości
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['title', 'content']


class NewMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['title', 'receiver', 'content']


# rejestracja nowego usera
class MyUserForm(UserCreationForm):
    groups = forms.ModelChoiceField(label='Rodzaj konta', queryset=Group.objects.all())

    class Meta:
        model = MyUser
        fields = ('username', 'first_name', 'last_name', 'email', 'groups')
        field_classes = {'username': UsernameField}


class MyUserChangeForm(UserChangeForm):

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name')


# formularz do logowania
class LoginForm(forms.Form):
    login = forms.CharField(max_length=50, label='login')
    password = forms.CharField(max_length=50, label='hasło', widget=forms.PasswordInput)
