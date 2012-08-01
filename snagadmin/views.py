from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from random import randint, shuffle, random, seed
from snag.genview import models
from sys import *
from snag.genview.models import Gens, Contents, Tasks
from django.utils.encoding import smart_str, smart_unicode
import math

#######################################################
# Home page
def main(request):
    # auth
    if request.user.is_authenticated():
        auth = "<p>User is authenticated as: <b>"+request.user.username+"</b></p>"

    else:
        auth = "<p>User is anonymous</p><p>Instructions for anonymous users here.</p>"

    return render_to_response('main.html', {'auth': auth})

