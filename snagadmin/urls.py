from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from snagadmin.views import main


urlpatterns = patterns('',
    (r'main$', main),
)
