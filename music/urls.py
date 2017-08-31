from django.conf.urls import url
from . import views
from .views import (
    ProfileUpdateView,
    )
app_name = 'music'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
   # url(r'^error/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<profile_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^search_bio/(?P<profile_id>[0-9]+)$', views.search_bio, name='search_bio'),
    # url(r'^(?P<song_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),
    url(r'^global_songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs_global, name='songs_global'),
    url(r'^create_profile/$', views.create_profile, name='create_profile'),
    url(r'^update_profile/(?P<pk>[0-9]+)/$',ProfileUpdateView.as_view(), name='update_profile'),
    url(r'^(?P<profile_id>[0-9]+)/create_song/$', views.create_song, name='create_song'),
    url(r'^(?P<profile_id>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/$', views.delete_song, name='delete_song'),
    url(r'^global_songs/(?P<filter_by>[a-zA_Z]+)/like_song/(?P<song_id>[\d]+)/$', views.like_song, name='like_song'),
    # url(r'^(?P<album_id>[0-9]+)/favorite_album/$', views.favorite_album, name='favorite_album'),
    #url(r'^(?P<album_id>[0-9]+)/delete_album/$', views.delete_album, name='delete_album'),
]
