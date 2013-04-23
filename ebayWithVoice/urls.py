from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ebayWithVoice.views.home', name='home'),
    # url(r'^ebayWithVoice/', include('ebayWithVoice.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^users/login$','users.views.login'),
    url(r'^users/logout$','users.views.logout'),
    url(r'^users/register$','users.views.register'),
    url(r'^users/newPage$','users.views.newPage'),
    url(r'^users/addFriend$','users.views.addFriend'),
    url(r'^users/showFriends$','users.views.showFriends'),
    
    url(r'^news/addNews$','news.views.addNews'),
    url(r'^news/getNewsList$','news.views.getNewsList'),
    url(r'^news/getPicture$','news.views.getPicture'),
    url(r'^news/getVoice$','news.views.getVoice'),
    url(r'^news/addComment$','news.views.addComment'),
    url(r'^news/deleteNews$','news.views.deleteNews'),
)
