from woofy.models import Announcement


def add_user_info(request):
    return {'user': request.user}


def announcements_list(request):
    all_announcements = Announcement.objects.all().order_by('-creation_date')
    return {'all_announcements': all_announcements}
