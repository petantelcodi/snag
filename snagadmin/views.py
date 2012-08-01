from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from random import randint, shuffle, random, seed
from snag.genview import models
from sys import *
from snag.genview.models import Gens, Contents, Tasks, Chromosome
from django.utils.encoding import smart_str, smart_unicode
import math

#######################################################
# Home page
def main(request):
    # auth
    if request.user.is_authenticated() and request.user.username == "admin":
        auth = "<p>Welcome <b>"+request.user.username+"</b></p>"

        # Getting and reordering Tasks
        tasksList = []
        for x in Tasks.objects.all():
            tasksList.append([smart_str(x.user_id), smart_str(x.chromosome_id_id), smart_str(x.test_date), smart_str(x.total_test_time), smart_str(x.test_ok) ])
        #for

    else:
        auth = "<p>This page is only accessible for admin users</p>"
        tasksList = []

    return render_to_response('main.html', {'auth': auth, 'tasksList': tasksList})

