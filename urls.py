from django.conf.urls.defaults import *

# snag. genview
from genview.views import *
#from registration import backends

# Added dajaxice
#from dajaxice.core import dajaxice_autodiscover
#dajaxice_autodiscover()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', home),
    # Example:
    # (r'^snag/', include('snag.foo.urls')),

    # Testpage
    (r'^testpage/', testpage),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # Added by django-registration
    (r'^accounts/', include('registration.backends.default.urls')),


    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    (r'admin/doc/', include('django.contrib.admindocs.urls'))

)
