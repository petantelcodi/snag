from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from snagadmin.views import *


urlpatterns = patterns('',
    # main admin interface
    (r'main$', main),

    # create a creature in generation 0 with 50 random chromosomes
    (r'createcreature$', createcreature),

    # user page
    (r'user$', userpage),
)
