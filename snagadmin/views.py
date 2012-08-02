from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from genview.models import Creature
from snag.genview.models import Gens, Contents, Tasks, Chromosome, Creature
from django.utils.encoding import smart_str, smart_unicode
from django.contrib.auth.models import User
import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from random import randint, shuffle, random, seed
from sys import *
import math

#######################################################
# Home page
def main(request):
    # auth
    if request.user.is_authenticated() and request.user.username == "admin":
        auth = "<p>Welcome <b>"+request.user.username+"</b></p>"

        # Getting Chromosomes list
        chromosomesList = []
        for c in Chromosome.objects.all():
            chromosomesList.append([smart_str(c.id), smart_str(c.data), smart_str(c.creature_id_id)])

        # Getting user list
        userList = []
        for u in User.objects.all():
            userList.append(smart_str(u.username))

        # Getting and reordering Tasks
        tasksList = []
        for x in Tasks.objects.all():
            tasksList.append([smart_str(x.user_id), smart_str(x.chromosome_id_id), smart_str(x.test_date), smart_str(x.total_test_time), smart_str(x.test_ok) ])


    else:
        auth = "<p>This page is only accessible for admin users</p>"
        tasksList = []
        userList = []
        chromosomesList = []

    return render_to_response('main.html', {'auth': auth, 'tasksList': tasksList, 'userList': userList, 'chromosomesList': chromosomesList})

#######################################################
# Create creature page
def createcreature(request):
    if request.user.is_authenticated() and request.user.username == "admin":
        auth = "<p>Welcome <b>"+request.user.username+"</b></p>"

        # Building 50 random chromosomes with 39 gens each of them with the structure 3x3x3
        struc_base = ["01", "0101", "010101", "010102", "010103", "0102", "010201", "010202", "010203", "0103", "010301", "010302", "010303", "02", "0201","020101", "020102", "020103", "0202", "020201", "020202", "020203", "0203", "020301", "020302", "020303", "03", "0301", "030101","030102", "030103","0302", "030201", "030202", "030203","0303", "030301", "030302", "030303",];
        tags_ids = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39"]
        chromosomes = []
        for n in range(1,3): ## FIXME this is for testiog. The good values is range(1,51)
            shuffle(tags_ids)
            chromosome = []
            c = 0
            for d in struc_base:
                chromosome.append(d+tags_ids[c])
                c = c + 1
            chromosomes.append(chromosome)
        # Inserting new creature in generation 0
        now = datetime.datetime.now()
        datenow = str(now.year)+'-'+str(now.month)+'-'+str(now.day)
        new = Creature.objects.create(creation_date=datenow, generation=0)
        new.save()
        # Inserting the new 50 chromosome
        mycreature = Creature.objects.latest('id')
        for c in chromosomes:
            entry = Chromosome(data=str(c), creature_id_id=str(mycreature))
            entry.save()

        # Getting Chromosomes list


    else:
        auth = "<p>This page is only accessible for admin users</p>"
        creature = []
        mycreature = 111

    return render_to_response('createcreature.html', {'auth': auth})

#######################################################
# Create creature page