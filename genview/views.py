from debian.debtags import output
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from random import randint, shuffle, random, seed
from snag.genview import models
from sys import *
from snag.genview.models import Gens, Contents, Tasks
from django.utils.encoding import smart_str, smart_unicode
import math
import json

#######################################################
# Home page
def home(request):
    # about
    about = ['un', 'dos', 'tres']

    # gen
    gen = []
    for alels in range(1, 33):
        gen.append(alels)
    shuffle(gen)

    # auth
    if request.user.is_authenticated():
        auth = "<p>User is authenticated as: <b>"+request.user.username+"</b></p>"

    else:
        auth = "<p>User is anonymous</p>"

    #about = models.Page.objects.get(id=1)
    #pics_list = models.Pic.objects.order_by('-id')[:49]
    ##r = randint(0, (len(pics_list)-1))
    ##pic_random = pics_list[r]
    return render_to_response('home.html', {'home': home, 'about': about, 'gen': gen, 'auth': auth})

#######################################################
def endtest(request):
    if request.method == 'POST':
        # You may process these variables here
        user_id = request.POST['user_id']
        chromosome_id = request.POST['chromosome_id']
        test_date = request.POST['test_date']
        total_test_time = request.POST['time']
        contents_id = request.POST['contents_id']
        test_ok = request.POST['test_ok']
        #Tasks.objects.create(test_ok=test_ok,user_id=user_id,contents_id=contents_id,total_test_time=total_test_time,test_date=test_date,chromosome_id=chromosome_id,user_id=user_id)
        #Tasks.objects.create(total_test_time=total_test_time)
        p = Tasks(test_ok=test_ok,contents_id_id=contents_id,total_test_time=total_test_time,test_date=test_date,chromosome_id_id=chromosome_id,user_id_id=user_id)
        p.save()
    if not request.user.is_authenticated():
        output = "<h1>You don't have direct access to this page!</h1>"
        template = 'home.html'
        username = ""
    else:
        output = ""
        template = 'endtest.html'
        username = request.user.username
    return render_to_response(template, {'username': username,'output': output } )    

#######################################################
def startAnel(request):
    data2 = [
                        ["0101",
                                [ "010102",[ "01010105", "01010208", "01010311"]],
                                [ "010203",[ "01020106", "01020209", "01020312"]],
                                [ "010304",[ "01030107", "01030210", "01030313"]]
                        ],
                        ["0214",
                                [ "020115",[ "02010118", "02010221", "02010324"]],
                                [ "020216",[ "02020119", "02020222", "02020325"]],
                                [ "020317",[ "02030120", "02030223", "02030326"]]
                        ],
                        ["0327",
                                [ "030128",[ "03010131", "03010234", "03010337"]],
                                [ "030229",[ "03020132", "03020235", "03020338"]],
                                [ "030330",[ "03030133", "03030236", "03030339"]]
                        ]
                ]


    return json.dumps(data2)
    
def starttest(request):
    """
    This function build a webpage for the test.
    First version id taking a fix gen data
    """
    #First, check if user is autetificated:
    if not request.user.is_authenticated():
        output = "<h1>You need to login before to take a test!</h1>"
        template = 'home.html'
        username = ""
        userid = ""
        questionTest = ""
        answersTest = ""
        idQuestion = ""
        genId = ""
    else:
        template = 'starttest.html'
        username = request.user.username
        userid = request.user.id
        data = ["0101", "010102", "01010105", "01010208", "01010311", "010203", "01020106", "01020209", "01020312", "010304", "01030107", "01030210", "01030313", "0214", "020115", "02010118", "02010221", "02010324", "020216", "02020119", "02020222", "02020325", "020317", "02030120", "0327", "030439", "030128", "03010131", "030229"];
        #tags = {1:"Acceso remoto (desde fuera de la universidad)", 2:"Archivo general", 3:"Archivo hist&oacute;rico", 4:"Archivos", 5:"Autenticaci&oacute;n en los servicios en l&iacute;nea", 6:"Bibliograf&iacute;as", 7:"Bibliograf&iacute;as por asignaturas", 8:"Bibliograf&iacute;as por materias", 9:"Bibliograf&iacute;as por titulaciones", 10:"Carn&eacute; de usuario", 11:"Colecci&oacute;n de libros electr&oacute;nicos", 12:"Colecciones", 13:"Derechos de autor", 14:"Fondo antiguo", 15:"Formaci&oacute;n", 16:"Formaci&oacute;n a medida", 17:"Formaci&oacute;n en l&iacute;nea", 18:"Gu&iacute;as", 19:"Gu&iacute;as por materias", 20:"Gu&iacute;as tem&aacute;ticas", 21:"Internet", 22:"Legislaci&oacute;n y jurisprudencia", 23:"Libros", 24:"Multimedia", 25:"Normativa de pr&eacute;stamo", 26:"Nuevas adquisiciones", 27:"Organismos de normalizaci&oacute;n", 28:"Partituras y grabaciones sonoras", 29:"Patentes", 30:"Pel&iacute;culas", 31:"Pr&eacute;stamo", 32:"Pr&eacute;stamo interbibliotecario", 33:"Recursos electr&oacute;nicos", 34:"Revistas", 35:"Revistas electr&oacute;nicas", 36:"Revistas impresas", 37:"Servicios", 38:"Talleres formativos", 39:"Zona Wi-Fi y Eduroam"}
        contents = {
            1:"<li>En la universidad existe acceso remoto</li><li>Tienen derecho al acceso remoto profesores, investigadores, estudiantes y personal administrativo</li><li>El acceso remoto permite consultar bases de datos cient&iacute;ficas y peri&oacute;dicos</li>",
            2:"<li>El archivo general se encuentra en el edificio de los servicios centrales</li><li>El archivo general se cre&oacute; en 1952</li><li>El archivo general alberga m&aacute;s de un mill&oacute;n de documentos</li>",
            3:"<li>El archivo hist&oacute;rico se encuentra en el edificio del rectorado</li><li>El archivo general se cre&oacute; en 1954</li><li>El archivo general alberga m&aacute;s de medio mill&oacute;n de documentos</li>",
            4:"<li>En la universidad existen dos tipos de archivo</li><li>Tienen derecho a los archivos profesores y personal administrativo</li><li>El responsable de los archivos es la Sra. Rodr&iacute;guez</li>",
            5:"<li>En lo servicios en linea se pueden autenticar profesores, estudiantes y personal de administraci&oacute;n</li><li>Para autenticarse en los servicios en l&iacute;nea se puede utilizar Explorer, Firefos, Chrome y Safari</li><li>Mediante la autenticaci&oacute;n se puede acceder a 6 servicios en l&iacute;nea</li>",
            6:"<li>En el servicvio de bibliograf&iacute;as trabajan 12 personas</li><li>El responsable del servicio de bibligraf&iacute;as es la Sra. Gonz&aacute;lez</li><li>El servicio de bilbliografias fue creado en 1981</li>",
            7:"<li>La extensi&oacute;n media de la bibliograf&iacute;a de una asignatura es de 20  referencias </li><li>El responsable del servicio de bibligraf&iacute;as por asignaturas es la Sra. Rodr&iacute;guez</li><li>El servicio de bilbliografias por asignaturas fue creado en 1982</li>",
            8:"<li>La extensi&oacute;n media de la bibliograf&iacute;a de una materia es de 500 referencias </li><li>El responsable del servicio de bibligraf&iacute;as por asignaturas es la Sra. Moreno</li><li>El servicio de bilbliografias por materias fue creado en 1983</li>",
            9:"<li>La extensi&oacute;n media de la bibliograf&iacute;a de una titulaci&oacute;n es de 2500 referencias </li><li>El responsable del servicio de bibligraf&iacute;as por titulaciones es la Sra. Garc&iacute;a</li><li>El servicio de bilbliografias por titulaciones fue creado en 1984</li>",
            10:"<li>Los colectivos de estudiantes, profesorado y personal de administraci&oacute;n son los que tienen derecho al carn&eacute; de usuario</li><li>El carn&eacute; de usuario se pueden utilizar en todos los centros que pertenecen a la Universidad</li><li>El carn&eacute; est&aacute; activo mientras que el usuario est&aacute; vinculado con la Universidad</li>",
            11:"<li>La colecci&oacute;n de libros electr&oacute;nicos alberga 10.500 titulos </li><li>El responsable de  la colecci&oacute;n de libros electr&oacute;nicos es la Sra. G&oacute;mez</li><li>La colecci&oacute;n de libros electr&oacute;nicos fue creada en 1995</li>",
            12:"<li>En el servicvio de colecci&oacute;nes trabajan 15 personas</li><li>El responsable del servicio de colecciones es la Sra. L&oacute;pez</li><li>El servicio de colecciones fue creado en 1985</li>",
            13:"<li>El responsable de los temas relacionados con los derechos de autor es la Sra. G&aacute;mez</li><li>En los temas relacionados con los derechos de autor trabajan 9 personas</li><li>En la universidad se aplica la pol&iacute;tica de derechos de autor que establece el Minsiterio de Cultura</li>",
            14:"<li>El fondo antiguo alberga 11.000 titulos </li><li>El responsable del fondo antiguo es la Sra. Garc&iacute;a</li><li>El fondo antiguo fue creado en 1975</li>",
            15:"<li>En la universidad existen dos tipos de formaci&oacute;n</li><li>Tienen derecho a la formaci&oacute;n estudiantes, profesores y personal administrativo</li><li>El responsable de la formaci&oacute;n es la Sra. Tr&iacute;as</li>",
            16:"<li>El servicio de formaci&oacute;n a medida se encuentra en el edificio de administraci&oacute;n</li><li>El servicio de formaci&oacute;n a medida se cre&oacute; en 1987</li><li>El email del servicio de formaci&oacute;n a medida es formacionamedida@universidad.edu</li>",
            17:"<li>El servicio de formaci&oacute;n en l&iacute;nea se encuentra en el edificio del rectorado</li><li>El servicio de formaci&oacute;n en l&iacute;nea se cre&oacute; en 1999</li><li>El email del servicio de formaci&oacute;n en l&iacute;nea es formacionenlinea@universidad.edu</li>",
            18:"<li>Existen dos tipos de gu&iacute;as</li><li>El servicio de las gu&iacute;as se cre&oacute; en 1998</li><li>El responsable de las gu&iacute;as la Sra. C&aacute;rdenas</li>",
            19:"<li>Existen 58 gu&iacute;as por materia </li><li>El responsable de las gu&iacute;as por materias es la Sra. Ruiz</li><li>El el servicio de gu&iacute;as por materias fue creada en 1999</li>",
            20:"<li>Existen 86 gu&iacute;as tem&aacute;ticas </li><li>El responsable de las gu&iacute;as tem&aacute;ticas es la Sra. Albarado</li><li>El el servicio de gu&iacute;as por materias fue creada en 2001</li>",
            21:"<li>En la universidad existe servicio de internet</li><li>Tienen derecho al servicio de internet profesores, investigadores, estudiantes y personal administrativo</li><li>El servicio de internet se ofrece desde 2002</li>",
            22:"<li>La biblioteca recibe puntualmente el BOE y el DOGC, y cuenta con los principales repertorios de legilaci&oacute;n y jurisprudencia.</li><li>Sobre legislaci&oacute;n y jurisprudencia existen varias bases de datos: Iberlex, DOGC y Eurlex.</li><li>El responsable del servicio de legislaci&oacute;n y jurisprudencia es la Sra. Serrano</li>",
            23:"<li>Los libros est&aacute;n organizados por materia, distribuidos f&iacute;sicamente seg&uacute;n la CDU.</li><li>Hay obras de consulta general y libros sobre las materias relacionadas con las titulaciones impartidas por la universidad.</li><li>La biblioteca dispone de 98.000 libros</li>",
            24:"<li>La biblioteca dispone de partituras, grabaciones sonoras y pel&iacute;culas. Adem&aacute;s, cuenta con un proyector de v&iacute;deo que puede salir en pr&eacute;stamo.</li><li>El lector de de DVD puede utilizarse &uacute;nicamente en la biblioteca</li><li>El responsable del material multimedia es la Sra. S&aacute;nchez</li>",
            25:"<li>Los retrasos en la devoluci&oacute;n de pr&eacute;stamos se penalizan a raz&oacute;n de un d&iacute;a por libro y d&iacute;a de retraso.</li><li>Los libros pueden salir en pr&eacute;stamo durante 30 d&iacute;as, excepto si son de pr&eacute;stamo restringido, en cuyo caso s&oacute;lo se prestan durante el fin de semana.</li><li>En caso de p&eacute;rdida o robo, el usuario se responsabiliza de reponer el material perdido.</li>",
            26:"<li>Entre las adquisiciones m&aacute;s recientes se incluyen los libros \"Vivir con la complejidad\", de Donald Norman, y \"Crisis y reconstrucci&oacute;n de la filosof&iacute;a\", de Mario Bunge.</li><li>La biblioteca ha incorporado tambi&eacute;n los DVD \"Break the Science Barrier\", de Richard Dawkins, y \"Inheriting the Future of Music\", de Gunter Atteln.</li><li>Destacan tambi&eacute;n como novedad los CD \"Das Lied von der Erde\", de Gustav Mahler, y \"R&eacute;pons\", de Pierre Boulez.</li>",
            27:"<li>Hay varios organismos de normalizaci&oacute;n europeos: entre otros, AENOR, AFNOR y DIN.</li><li>En Latinoam&eacute;rica hay NORMEX, AMN e IRAM, entre otros.</li><li>En Catalunya hay dos asociaciones de normas t&eacute;cnicas: ACEIC e ICT.</li>",
            28:"<li>La biblioteca dispone de una colecci&oacute;n de partituras y grabaciones sonoras.</li><li>Las partituras est&aacute;n archivadas en carpetas, en la secci&oacute;n de m&uacute;sica.</li><li>Hay 4 puntos de audici&oacute;n para la escucha de grabaciones sonoras.</li>",
            29:"<li>Hay 3 oficinas de patentes: EPO European Patent Office, Oficina Espanola de Patentes y Marcas, y World Intellectual Property Organization </li><li>Existen varias bases de datos de patentes: Delphion, Derwent Innovation Index y FreePatentsOnline.</li><li>Para obtener documentos de patente hay que dirigirse al servicio de pr&eacute;stamo interbibliotecario.</li>",
            30:"<li>La biblioteca tiene una colecci&oacute;n de pel&iacute;culas de todas las &eacute;pocas.</li><li>Las pel&iacute;culas est&aacute;n en la secci&oacute;n de cine y audiovisuales.</li><li>Este material est&aacute; disponible &uacute;nicamente en DVD.</li>",
            31:"<li>Pueden utilizar el servicio de pr&eacute;stamo profesores, investigadores, estudiantes y personal administrativo.</li><li>Pueden salir en pr&eacute;stamo los libros, los DVD y el material multimedia.</li><li>Tienen derecho al servicio de pr&eacute;stamo profesores, investigadores, estudiantes y personal administrativo</li>",
            32:"<li>Pueden utilizar el servicio de pr&eacute;stamo interbibliotecario s&oacute;lo profesores e investigadores.</li><li>El material solicitado suele servirse en el plazo de 1 a 2 d&iacute;as.</li><li>El material prestado mediante pr&eacute;stamo interbibliotecario se puede devolver en cualquier biblioteca de la universidad.</li>",
            33:"<li>La biblioteca ofrece acceso a recursos electr&oacute;nicos diversos: bibliograf&iacute;as, gu&iacute;as, bases de datos, etc.</li><li>Los recursos generados por la biblioteca son de acceso abierto; entre los dem&aacute;s los hay gratuitos y de pago.</li><li>El responsable de los servicios electr&oacute;nicos es la Sra. Mart&iacute;nez</li>",
            34:"<li>La biblioteca mantiene suscripci&oacute;n a 200 revistas cient&iacute;ficas.</li><li>La mayor&iacute;a de las revistas suscritas est&aacute;n disponibles en papel; las dem&aacute;s son accesibles en soporte electr&oacute;nico.</li><li>El responsable de las revistas es la Sra. V&aacute;zquez</li>",
            35:"<li>Desde la biblioteca se pueden consultar gratuitamente 60 revistas electr&oacute;nicas de pago: EPI, Journal of Documentation y otras.</li><li>De acceso abierto existen muchas revistas electr&oacute;nicas: Ariadne, BiD y otras.</li><li>Para localizar una revista electr&oacute;nica sobre un tema concreto se puede utilizar el cat&aacute;logo de la biblioteca.</li>",
            36:"<li>En la biblioteca se pueden consultar completas 140 revistas impresas: &Iacute;tem, Medicine y otras.</li><li>Los n&uacute;meros antiguos (m&aacute;s de 2 anos) se guardan en el archivo y se han de solicitar al personal bibliotecario.</li><li>El responsable de las revistas impresas es la Sra. Vi&oacute;zquez</li>",
            37:"<li>La biblioteca ofrece diversos servicios: pr&eacute;stamo, formaci&oacute;n y acceso a Internet.</li><li>Los servicios, en general, est&aacute;n abiertos a la comunidad universitaria: profesores, investigadores, estudiantes y personal administrativo.</li><li>Todos ellos son de uso gratuito.</li>",
            38:"<li>La biblioteca ofrece talleres formativos sobre el uso del cat&aacute;logo y el acceso a bases de datos cient&iacute;ficas.</li><li>Los talleres presenciales se programan la segunda semana de cada mes, excepto en agosto. Los virtuales, la cuarta semana.</li><li>Para inscribirse, basta con usar el formulario habilitado a tal efecto.</li>",
            39:"<li>Pueden utilizar la red Wi-Fi profesores, investigadores, estudiantes y personal administrativo.</li><li>Todos los espacios de la biblioteca tiene cobertura para la conexi&oacute;n inal&aacute;mbrica a Internet.</li><li>La biblioteca ofrece conexi&oacute;n v&iacute;a Eduroam a la comunidad universitaria y a visitantes procedentes de instituciones afiliadas a esta inciativa."
        }
        
        #choose a question
        idQuestion = randint(1, 39*3)
        answers = []
        questions = []
        for x in Contents.objects.all():
            questions.append(smart_str(x.question))
            answers.append(smart_str(x.answers))
            
        questionTest = questions[idQuestion]
        answersTest = answers[idQuestion]
        idQuestion = idQuestion%3;
        genId = int(idQuestion/3);
        
        tags = []
        for x in Gens.objects.all():
            tags.append(smart_str(x.name))

        output = ""
        mytree = dict()
        for allele in data:
            # prefix -> position
            pre = allele[:(len(allele)-2)]
            # sufix -> id
            suf = allele[(len(allele)-2):len(allele)]
            #print allele+" = "+pre+" + "+suf
            mytree[suf] = pre

        # frist nav bar
        first = []
        nav1 = "<div id='nav1'><p>"
        con = "<div id='hiddencontents'>"
        for  k in mytree.keys():
            knum = int(k)
            if len(mytree[k]) == 2:
                nav1 = nav1+"\n\t<span id='"+str(k)+"-"+mytree[k]+"' class='first'>"+str(tags[knum])+"</span>"
                infos = ""
                c = 1
                for i in contents[knum].split("</li><li>"):
                    button = "&nbsp;<input type='button' class='b' size='10' value='"+str(k)+"-"+mytree[k]+"-"+str(c)+"'>"
                    infos = infos+"<li>"+i+button+"</li>"
                    c = c+1
                con = con+"\n\t<div id='c-"+str(k)+"-"+mytree[k]+"'>"+infos[4:]+"</div>"
                first.append(mytree[k])

        nav1 = nav1+"\n</p></div>"
        output = output+nav1

        # second nav bar
        second = []
        nav2 = "<div id ='nav2'><ul>"
        for f in first:
            for  k in mytree.keys():
                knum = int(k)
                if f == mytree[k][0:len(f)] and len(mytree[k]) == 4:
                    nav2 = nav2+"\n\t<li id='"+str(k)+"-"+mytree[k]+"' class='"+str(f)+" second'>"+str(tags[knum])+"</li>"
                    infos = ""
                    c = 1
                    for i in contents[knum].split("</li><li>"):
                        button = "&nbsp;<input type='button' class='b' size='10' value='"+str(k)+"-"+mytree[k]+"-"+str(c)+"'>"
                        infos = infos+"<li>"+i+button+"</li>"
                        c = c+1
                    con = con+"\n\t<div id='c-"+str(k)+"-"+mytree[k]+"'>"+infos+"</div>"
                    second.append(mytree[k])

        nav2 = nav2+"\n</ul></div>\n"
        output = output+nav2

        # third nav bar
        third = []
        nav3 = "<div id ='nav3'><ul>"
        for f in second:
            for  k in mytree.keys():
                knum = int(k)
                if f == mytree[k][0:len(f)] and len(mytree[k]) == 6:
                    nav3 = nav3+"\n\t<li id='"+str(k)+"-"+mytree[k]+"' class='"+str(f)+" third'>"+str(tags[knum])+"</li>"
                    infos = ""
                    c = 1
                    for i in contents[knum].split("</li><li>"):
                        button = "&nbsp;<input type='button' class='b' size='10' value='"+str(k)+"-"+mytree[k]+"-"+str(c)+"'>"
                        infos = infos+"<li>"+i+button+"</li>"
                        c = c+1
                    con = con+"\n\t<div id='c-"+str(k)+"-"+mytree[k]+"'>"+infos+"</div>"

        nav3 = nav3+"\n</ul></div>\n"
        nav3 = nav3+"<div id='contents'><ul></ul></div>\n"
        con = con+"\n</div>\n"
        output = output+nav3+con
        
    return render_to_response(template, {'username': username,'userid': userid,'questionTest': questionTest,'answersTest':answersTest,'idQuestion':idQuestion,'genId':genId,'output': output } )

#######################################################
def profile(request):

    if request.user.is_authenticated():
        auth = "<p>User profile.</p>"
        auth += "<p>Hello {{ user.username }}. User is authenticated</p>"
    else:
        auth = "<p>User is anonymous</p>"

    return render_to_response('profile.html', {'auth': auth })

#######################################################
def myexample(request):
    '''
    test getting data from ddbb
    '''
    #Base emptey chromosome 3x3x3 structure:
    data_base = ["01", "0101", "010101", "010102", "010103", "0102", "010201", "010202", "010203", "0103", "010301", "010302", "010303", "02", "0201","020101", "020102", "020103", "0202", "020201", "020202", "020203", "0203", "020301", "020302", "020303", "03", "0301", "030101","030102", "030103","0302", "030201", "030202", "030203","0303", "030301", "030302", "030303",];
    tags = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39"]
    shuffle(tags)
    mydata = []
    c = 0
    for d in data_base:
        mydata.append(d+tags[c])
        c = c + 1

    return render_to_response('myexample.html', {'mydata': mydata})

#######################################################
def testpage(request):
    if request.user.is_authenticated():
        auth = "<p>User is authenticated</p>"
    else:
        auth = "<p>User is anonymous</p>"

    return render_to_response('testpage.html', {'testpage': testpage, 'auth': auth})

'''
# Conversations
def conversations_list(request):
    about = models.Page.objects.get(id=1)
    conversations_list = models.Conversation.objects.order_by('-date')
    ##pics_in_conversation = get_list_or_404(models.Pic.objects.order_by('-conversation'))
    paginator = Paginator(conversations_list, 4)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        conversations_list_pag = paginator.page(page)
    except (EmptyPage, InvalidPage):
        conversations_list_pag = paginator.page(paginator.num_pages)
    return render_to_response('latest_conversations.html', {'about': about, 'conversations_list': conversations_list, 'conversations_list_pag': conversations_list_pag })

def conversation_item(request, conversation_id):
    conversation_item = get_object_or_404(models.Conversation, pk=conversation_id)
    return render_to_response('conversation_item.html', { 'conversation_item' : conversation_item })
    #parts = get_list_or_404(models.Participant, conversation=conversation_id)
    #return render_to_response('conversation_item.html', { 'parts': parts, 'conversation_item' : conversation_item,})

# Participants
def participants_list(request):
    participants_list = models.Participant.objects.order_by('-last_name')
    paginator = Paginator(participants_list, 4)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        participants_list_pag = paginator.page(page)
    except (EmptyPage, InvalidPage):
        participants_list_pag = paginator.page(paginator.num_pages)

    return render_to_response('participants_list.html', {'participants_list': participants_list, 'participants_list_pag': participants_list_pag})

def participant_item(request, participant_id):
    participant_item = get_object_or_404(models.Participant, pk=participant_id)
    in_conversations = get_list_or_404(models.Conversation.objects.order_by('-date'), participants=participant_id)
    #in_conversations =''
    return render_to_response('participant_item.html', {'participant_item': participant_item, 'in_conversations': in_conversations })

'''
