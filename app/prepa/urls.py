from django.conf.urls import patterns, include, url

urlpatterns = patterns('prepa.views',
    url(r'^$', 'update'),
)
