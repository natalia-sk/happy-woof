from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from woofy.forms import AddNewPostForm, LoginForm, MyUserForm, AddNewAnnouncementForm, AddServicePageForm, \
    CommentForm, MessageForm, MyUserChangeForm, NewMessageForm
from woofy.models import WoofyPost, ServicePage, CATEGORIES, Comment, Announcement, Message


class AllPostView(View):
    def get(self, request):
        all_posts = WoofyPost.objects.all().order_by('-creation_date')
        all_comments = Comment.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(all_posts, 5)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        ctx = {'posts': posts,
               'all_coments': all_comments}
        return render(request, 'woofy/all_posts.html', ctx)


class PostDetailsView(View):
    def get(self, request, post_id):
        form = CommentForm()
        post = WoofyPost.objects.get(id=post_id)
        comments = Comment.objects.filter(post_id=post_id).order_by('-creation_date')
        user = request.user
        ctx = {'form': form,
               'post': post,
               'comments': comments,
               'user': user}
        return render(request, 'woofy/post_details.html', ctx)

    def post(self, request, post_id):
        form = CommentForm(request.POST)
        post = WoofyPost.objects.get(id=post_id)
        comments = Comment.objects.filter(post_id=post_id).order_by('-creation_date')
        if form.is_valid():
            Comment.objects.create(content=form.cleaned_data['content'], user=request.user, post_id=post.id)
            form = CommentForm()
            ctx = {'form': form, 'post': post, 'comments': comments}
            return render(request, 'woofy/post_details.html', ctx)
        else:
            ctx = {'form': form, 'post': post, 'comments': comments}
            return render(request, 'woofy/post_details.html', ctx)


class AddNewPostView(View):
    """
    Adding new post only for logged in users
    """

    @method_decorator(login_required)
    def get(self, request):
        form = AddNewPostForm()
        return render(request, 'woofy/add_post.html', {'form': form})

    def post(self, request):
        form = AddNewPostForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('index')
        return render(request, 'woofy/add_post.html', {'form': form})


class PostDeleteView(View):
    @method_decorator(login_required)
    def get(self, request, post_id):
        return render(request, 'woofy/woofypost_confirm_delete.html')

    def post(self, request, post_id):
        post = WoofyPost.objects.get(id=post_id)
        if request.POST.get('delete') == 'usuń':
            post.delete()
            return redirect('index')
        return redirect('index')


class CommentDeleteView(View):
    @method_decorator(login_required)
    def get(self, request, comment_id):
        return render(request, 'woofy/comment_confirm_delete.html')

    def post(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id)
        if request.POST.get('delete') == 'usuń':
            comment.delete()
            return redirect('/')
        return redirect('/')


class AllAnnouncementView(View):
    def get(self, request):
        return render(request, 'woofy/all_announcements.html')


class AnnouncementDetailsView(View):
    def get(self, request, announcement_id):
        announcement = Announcement.objects.get(id=announcement_id)
        return render(request, 'woofy/announcement_details.html', {'announcement': announcement})


class AnnouncementDeleteView(View):
    @method_decorator(login_required)
    def get(self, request, announcement_id):
        return render(request, 'woofy/announcement_confirm_delete.html')

    def post(self, request, announcement_id):
        announcement = Announcement.objects.get(id=announcement_id)
        if request.POST.get('delete') == 'usuń':
            announcement.delete()
            return redirect('index')
        return redirect('index')


class AddNewAnnouncementView(View):
    """
    Adding new announcement, only for logged in users
    """

    @method_decorator(login_required)
    def get(self, request):
        form = AddNewAnnouncementForm()
        return render(request, 'woofy/add_announcement.html', {'form': form})

    def post(self, request):
        form = AddNewAnnouncementForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('announcements')
        return render(request, 'woofy/add_announcement.html', {'form': form})


# widok wszystkich stron usługodawców
class ServicePageListView(View):
    def get(self, request):
        service_pages = ServicePage.objects.all().order_by('name')
        categories = dict(CATEGORIES)
        ctx = {'service_pages': service_pages,
               'categories': categories}
        return render(request, 'woofy/service_pages_list.html', ctx)


# szczegółowy widok strony usługodawcy
class ServicePageDetailsView(View):
    def get(self, request, page_id):
        page = ServicePage.objects.get(id=page_id)
        categories = dict(CATEGORIES)
        ctx = {'page': page,
               'categories': categories}
        return render(request, 'woofy/service_pages_details.html', ctx)


class AddServicePageView(View):
    @method_decorator(permission_required('woofy.add_servicepage'))
    def get(self, request):
        form = AddServicePageForm()
        return render(request, 'woofy/add_service_page.html', {'form': form})

    def post(self, request):
        form = AddServicePageForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('service-pages')
        return render(request, 'woofy/add_service_page.html', {'form': form})


class ServicePageDeleteView(View):
    @method_decorator(permission_required('woofy.delete_servicepage'))
    def get(self, request, page_id):
        return render(request, 'woofy/servicepage_confirm_delete.html')

    def post(self, request, page_id):
        page = ServicePage.objects.get(id=page_id)
        if request.POST.get('delete') == 'usuń':
            page.delete()
            return redirect('index')
        return redirect('service-pages')


class UserDetailsView(View):
    @method_decorator(login_required)
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        posts = WoofyPost.objects.filter(user_id=user.id).order_by('-creation_date')
        pages = ServicePage.objects.filter(user_id=user.id).order_by('name')
        announcements = Announcement.objects.filter(user_id=user.id).order_by('-creation_date')
        comments = Comment.objects.filter(user_id=user.id).order_by('-creation_date')
        r_messages = Message.objects.filter(receiver_id=user.id).order_by('-creation_date')
        s_messages = Message.objects.filter(sender_id=user.id).order_by('-creation_date')
        ctx = {'user': user,
               'posts': posts,
               'pages': pages,
               'announcements': announcements,
               'comments': comments,
               'r_messages': r_messages,
               's_messages': s_messages}
        return render(request, 'woofy/user_details.html', ctx)


class EditUserDetailsView(View):
    @method_decorator(login_required)
    def get(self, request, user_id):
        form = MyUserChangeForm(instance=request.user)
        return render(request, 'woofy/edit_user.html', {'form': form})

    def post(self, request, user_id):
        form = MyUserChangeForm(request.POST)
        user = User.objects.get(id=user_id)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            return redirect('user-details', user_id)
        return render(request, 'woofy/edit_user.html', {'form': form})


class ChangeUserPasswordView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, 'woofy/password.html', {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            u = form.save()
            login(request, u)
            return redirect('/')
        return render(request, 'woofy/password.html', {'form': form})


class MessageDetailView(View):
    @method_decorator(login_required)
    def get(self, request, user_id, message_id):
        user = User.objects.get(id=user_id)
        msg = Message.objects.get(id=message_id)
        sender = User.objects.get(id=msg.sender_id)
        receiver = User.objects.get(id=msg.receiver_id)
        r_messages = Message.objects.filter(receiver_id=user.id).order_by('-creation_date')
        s_messages = Message.objects.filter(sender_id=user.id).order_by('-creation_date')
        form = MessageForm()
        ctx = {'user': user,
               'msg': msg,
               'r_messages': r_messages,
               's_messages': s_messages,
               'sender': sender,
               'receiver': receiver,
               'form': form}
        return render(request, 'woofy/msg_details.html', ctx)

    def post(self, request, user_id, message_id):
        form = MessageForm(request.POST)
        user = User.objects.get(id=user_id)
        msg = Message.objects.get(id=message_id)
        sender = User.objects.get(id=msg.sender_id)
        receiver = User.objects.get(id=msg.receiver_id)
        r_messages = Message.objects.filter(receiver_id=user.id).order_by('-creation_date')
        s_messages = Message.objects.filter(sender_id=user.id).order_by('-creation_date')
        if form.is_valid():
            Message.objects.create(sender=request.user,
                                   receiver_id=sender.id,
                                   title=form.cleaned_data['title'],
                                   content=form.cleaned_data['content'])
            form = MessageForm()
            ctx = {'user': user,
                   'msg': msg,
                   'r_messages': r_messages,
                   's_messages': s_messages,
                   'sender': sender,
                   'receiver': receiver,
                   'form': form}
            return render(request, 'woofy/msg_details.html', ctx)
        else:
            ctx = {'user': user,
                   'msg': msg,
                   'r_messages': r_messages,
                   's_messages': s_messages,
                   'sender': sender,
                   'receiver': receiver,
                   'form': form}
            return render(request, 'woofy/msg_details.html', ctx)


class NewMessageView(View):
    def get(self, request):
        form = NewMessageForm(instance=request.user)
        return render(request, 'woofy/msg_send.html', {'form': form})

    def post(self, request):
        form = NewMessageForm(request.POST)
        if form.is_valid():
            new_msg = Message.objects.create(sender=request.user,
                                             receiver=form.cleaned_data['receiver'],
                                             title=form.cleaned_data['title'],
                                             content=form.cleaned_data['content'])
            new_msg.save()
            return redirect('user-details', request.user.id)
        return render(request, 'woofy/msg_send.html', {'form': form})


class UserCreationView(View):
    def get(self, request):
        form = MyUserForm()
        return render(request, 'woofy/add_user.html', {'form': form})

    def post(self, request):
        form = MyUserForm(request.POST)
        if form.is_valid():
            u = form.save()
            login(request, u)
            user = User.objects.get(username=form.cleaned_data['username'])
            user_group = Group.objects.get(name=form.cleaned_data['groups'])
            user.groups.add(user_group)
            return redirect('index')
        return render(request, 'woofy/add_user.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'woofy/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
            form.add_error('password', ['Błędne hasło.'])
        return render(request, 'woofy/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class Error404View(View):
    def get(self, request):
        return render(request, 'woofy/error404.html')
