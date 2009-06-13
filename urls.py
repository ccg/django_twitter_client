from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^django_twitter_oauth_test/', include('django_twitter_oauth_test.foo.urls')),
    (r'^$', 'django_twitter_oauth_test.main.views.index'),
    (r'twitter', include('twitter_app.urls')),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)
