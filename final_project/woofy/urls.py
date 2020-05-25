from django.urls import path, re_path

from happy_woof import settings
from woofy.views import AllPostView, LoginView, LogoutView, UserCreationView, AddNewPostView, AddNewAnnouncementView, \
    ServicePageListView, ServicePageDetailsView, AddServicePageView, PostDetailsView, UserDetailsView, \
    MessageDetailView, PostDeleteView, CommentDeleteView, AnnouncementDeleteView, AnnouncementDetailsView, \
    ServicePageDeleteView, Error404View, EditUserDetailsView, ChangeUserPasswordView, NewMessageView, AllAnnouncementView
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', AllPostView.as_view(), name='index'),
    path('all_announcements', AllAnnouncementView.as_view(), name='announcements'),
    path('service_pages/', ServicePageListView.as_view(), name='service-pages'),

    # details
    path('post_details/<int:post_id>/', PostDetailsView.as_view(), name='post-details'),
    path('service_pages/<int:page_id>/', ServicePageDetailsView.as_view(), name='service-page-details'),
    path('msg_details/<int:user_id>/<int:message_id>/', MessageDetailView.as_view(), name='msg-details'),
    path('announcement_details/<int:announcement_id>/', AnnouncementDetailsView.as_view(), name='announcement-details'),

    # add new/send new
    path('add_post/', AddNewPostView.as_view(), name='add-post'),
    path('add_announcement/', AddNewAnnouncementView.as_view(), name='add-announcement'),
    path('add_service_page/', AddServicePageView.as_view(), name='add-service-page'),
    path('add_service_page/', AddServicePageView.as_view(), name='add-service-page'),
    path('new_msg/', NewMessageView.as_view(), name='new-message'),

    # delete
    path('post_delete/<int:post_id>/', PostDeleteView.as_view(), name='post-delete'),
    path('comment_delete/<int:comment_id>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('announcement_delete/<int:announcement_id>/', AnnouncementDeleteView.as_view(), name='announcement-delete'),
    path('service_page_delete/<int:page_id>/', ServicePageDeleteView.as_view(), name='page-delete'),

    # users
    path('join_in/', UserCreationView.as_view(), name='join-in'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user_details/<int:user_id>/', UserDetailsView.as_view(), name='user-details'),
    path('edit_user/<int:user_id>/', EditUserDetailsView.as_view(), name='edit-user'),
    path('edit_user/password/', ChangeUserPasswordView.as_view(), name='edit-password'),

    # 404
    re_path(r'^[\w\/_-]+$', Error404View.as_view(), name='error')

]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
