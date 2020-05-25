from woofy.models import Announcement
from django.contrib.auth.models import Group


def add_user_info(request):
    if len(Group.objects.filter(user=request.user.id)) == 0:
        user_group = "-"
    else:
        user_group = Group.objects.get(user=request.user.id).name
    return {'user': request.user, 'group': user_group}


def announcements_list(request):
    all_announcements = Announcement.objects.all().order_by('-creation_date')
    return {'all_announcements': all_announcements}
