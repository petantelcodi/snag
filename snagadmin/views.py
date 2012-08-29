from django.contrib.gis.gdal.prototypes import generation
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from genview.models import Creature
from snag.genview.models import Tasks, Chromosome, Creature
from django.utils.encoding import smart_str, smart_unicode
from django.contrib.auth.models import User
import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from random import randint, shuffle, random, seed
from django.db import reset_queries, close_connection
from sys import *
import math

#######################################################
# Home page
def main(request):
    tasksList = []
    userList = []
    chromosomesList = []
    creatureListInProcess = []
    creatureListFinished = []
    form_response = ''
    auth = ''
    go = ''
    new_creature = ''
    # auth
    if request.user.is_authenticated() and request.user.username == "admin":
        auth = "<p>Welcome <b>"+request.user.username+"</b></p>"
        go = 'main.html'
        # Check if this is an AJAX call and proceed:
        if request.is_ajax() or request.method == 'POST':
            #return HttpResponse("Success")
            myCreatureId = request.POST.get('chr')
            myUserId_name = request.POST.get('s')
            myUserIdl = myUserId_name.split("-")
            myUserId = myUserIdl[0]
            #myUserId = myUserId_name[0]
            form_response = ''
            # Assigning User to Chromosome:
            if str(myUserId_name)=='0':
                form_response='<div id="form_response"><b>You must choose a user from dropdwon menu!</b></div>'
            else:

                for m in Chromosome.objects.filter(creature_id=myCreatureId):
                    m.user_id_id=myUserId
                    m.save()
                    form_response = '<div id="form_response">Chromosome id <b>'+str(myCreatureId)+'</b> has been assigned to user <b>'+str(myUserId_name)+' | '+str(myUserId)+'</b></div>'
                    t = Tasks.objects.get(chromosome_id=m.id)
                    t.user_id_id=myUserId
                    t.save()

        # getting the number of finished Creatures (current generation = 50
        creatureListFinished = []
        for creature in Creature.objects.filter(current_generation__gte='20'):
            creatureListFinished.append([smart_str(creature.id), smart_str(creature.creation_date), smart_str(creature.current_generation)])

        # Getting user list
        userList = []
        for u in User.objects.all():
            userList.append([smart_str(u.id), smart_str(u.username)])
        # HTML <select> dropdows nuild upon user list
        #select = '<select id="" name="myselect"><option value="0"><-- Select One --></option>'
        options = ''
        for u in userList:
            options = options+'<option value="'+u[0]+'-'+u[1]+'">'+u[1]+'</option>'


        # Getting Chromosomes list:
        chromosomesList = []
        submit_b = ''
        count = 0
        for c in Chromosome.objects.all():
            if c.user_id_id==0:
                #myusername = '<form method="POST" action="/snagadmin/main" id="form-'+str(c.id)+'"><select name="s"><option value="0"><-- Select One --></option>'+options+'z/select>'
                #submit_b = '<input type="submit" id="send_form-'+str(c.id)+'" name="chr" value="'+str(c.id)+'"></form>'  # submit button to assig user to chromosome/generation
                pass
            else:
                #myusername = User.objects.get(id=c.user_id_id)
                #submit_b = ''
                pass
            count = count + 1
            chromosomesList.append([smart_str(c.id), smart_str(c.creature_id_id), smart_str(c.generation), smart_str(c.user_id_id)])

        # Getting and reordering Tasks
        tasksList = []
        for x in Tasks.objects.all():
            tasksList.append([smart_str(x.user_id_id), smart_str(x.chromosome_id_id), smart_str(x.test_date), smart_str(x.total_test_time), smart_str(x.test_ok) ])

        # getting Creatures with generation > 0:
        #creatureListInProcess = []
        #for creature in Creature.objects.filter(current_generation__lte ='19'):
        #    creatureListInProcess.append([smart_str(creature.id), smart_str(creature.creation_date), smart_str(creature.current_generation)])
        creatureListInProcess = []
        for creature in Chromosome.objects.raw("SELECT DISTINCT  `creature_id_id`, `id` FROM  `genview_chromosome` WHERE  `user_id_id` =0 group by `creature_id_id`;"):
            #raw("SELECT DISTINCT  `creature_id_id` FROM  `genview_chromosome` WHERE  `user_id_id` =0 group by `creature_id_id`;"):
            #filter(user_id=0).order_by('creature_id').distinct('creature_id'):
            #FIXME : it needs a relacional query: select distinct creature in table Chromosomes where creature_id=creature.id
            myusername = '<form method="POST" action="/snagadmin/main" id="form-'+str(creature.creature_id)+'"><select name="s"><option value="0"><-- Select One --></option>'+options+'z/select>'
            submit_b = '<input type="submit" id="send_form-'+str(creature.creature_id)+'" name="chr" value="'+str(creature.creature_id)+'"></form>'  # submit button to assig user to chromosome/generation
            creatureListInProcess.append([smart_str(creature.creature_id), smart_str(creature.generation), smart_str(creature.user_id_id), smart_str(myusername), submit_b])


    else:
        auth = "<p>This page is only accessible for admin users</p>"
        go = "noaccess.html"
    return render_to_response(go, {'form_response':form_response, 'auth': auth, 'tasksList': tasksList, 'userList': userList, 'chromosomesList': chromosomesList, 'creatureListInProcess': creatureListInProcess, 'creatureListFinished': creatureListFinished})

#######################################################
# Create creature page
def createcreature(request):

    # vars:
    auth = "<p>This page is only accessible for admin users</p>"
    creature = []
    mycreature = []
    go = 'createcreature.html'

    if request.user.is_authenticated() and request.user.username == "admin":
        auth = "<p>Welcome <b>"+request.user.username+"</b></p>"
        go = 'createcreature.html'
        userid = request.user.id

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
        # Inserting new creature (generation 0) in Creature Table
        now = datetime.datetime.now()
        datenow = str(now.year)+'-'+str(now.month)+'-'+str(now.day)
        new = Creature.objects.create(creation_date=datenow, current_generation=0)
        new.save()
        # Inserting the new 50 chromosome and the new 50 pending tasks in Tasks
        mycreature = Creature.objects.latest('id')
        for c in chromosomes:
            newChromosomes = Chromosome(data=str(c), creature_id_id=str(mycreature))
            newChromosomes.save()
            latestId=newChromosomes.id
            newTasks = Tasks(user_id_id=0, chromosome_id_id=str(latestId))
            newTasks.save()


        # Getting Chromosomes list

    else:
        auth = "<p>This page is only accessible for admin users</p>"
        go = 'noaccess.html'

    return render_to_response(go, {'auth': auth, 'mycreature': mycreature})

#######################################################
# User page
def userpage(request):
    #vars:
    username = ''
    userid = ''
    chromosomeListInProcess = []
    chromosomeListFinished = []
    tasksDone = []
    tasksPending = []

    if request.user.is_authenticated():
        auth = "<p>Welcome <b>"+request.user.username+"</b></p>"
        go = 'userpage.html'
        username = request.user.username
        userid = request.user.id

        ## List of pending chromosomes for the username
        mychromosome = Chromosome.objects.raw("SELECT DISTINCT  `creature_id_id`, `id` FROM  `genview_chromosome` WHERE  `user_id_id` ='"+str(userid)+"' group by `creature_id_id`;")
        #filter(generation__lte='19', user_id=userid).order_by('creature_id').distinct('creature_id_id')
        #mychromosome.group_by = ['creature_id_id']
        for c in mychromosome:
            chromosomeListInProcess.append([smart_str(c.creature_id), smart_str(c.generation)])
        ## List of finished chromosomes for the user
        mychromosome1 = Chromosome.objects.filter(generation='20', user_id=userid)
        for c in mychromosome1:
            chromosomeListFinished.append([smart_str(c.creature_id), smart_str(c.generation)])

        ## List of your pending tasks
        for task in Tasks.objects.filter(user_id=userid).filter(test_done=0):
            tasksPending.append([smart_str(task.chromosome_id_id), smart_str(task.test_date), smart_str(task.total_test_time), smart_str(task.test_ok)])


        ## List of tasks done for the username
        for task in Tasks.objects.filter(user_id=userid).filter(test_done__gte=1):
            tasksDone.append([smart_str(task.chromosome_id_id), smart_str(task.test_date), smart_str(task.total_test_time), smart_str(task.test_done)])

    else:
        auth = "<p>This page is only accessible for authetificated users</p>"
        go = 'noaccess.html'

    return render_to_response(go, {'auth': auth, 'username':username, 'chromosomeListInProcess': chromosomeListInProcess, 'chromosomeListFinished': chromosomeListFinished, 'tasksDone':tasksDone, 'tasksPending': tasksPending})