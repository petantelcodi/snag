from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from random import randint, shuffle, random, seed
from snag.genview.models import Tasks, Contents, Chromosome
from snag.snagadmin.views import config
from snag.genetics.views import genetics
from django.utils.encoding import smart_str, smart_unicode
import math
import operator
from django.db import connection
from snag.settings import MEDIA_URL

#######################################################
# Home page
def home(request):
    # auth
    if request.user.is_authenticated():
        auth = "<p>User is authenticated as: <b>"+request.user.username+"</b></p>"

    else:
        auth = "<p>You are an anonymous user.</p><p>Login is required in order to participate. Please register or login.</p><p>Instructions for anonymous users here ...</p><p>...</p><p>...</p><p>...</p>"

    return render_to_response('home.html', {'home': home, 'auth': auth})

#######################################################
def endtest(request):
    # vars:
    mychromosome_id = ''
    generation_x_creature = config("GENERATION_X_CREATURE")

    if request.method == 'POST':
        # You may process these variables here
        user_id = request.POST['user_id']
        mychromosome_id = request.POST['chromosome_id']
        mytest_date = request.POST['test_date']
        mytotal_test_time = request.POST['time']
        mytest_ok = request.POST['test_ok']

    if not request.user.is_authenticated():
        output = "<h1>Sorry, you don't have direct access to this page!</h1>"
        template = 'home.html'
        username = ""
    else:
        if mychromosome_id:
            # Save the test results in Tasks table, where chromosome_id_id=chromosome_id
            Tasks.objects.filter(chromosome_id=mychromosome_id).update(test_ok=mytest_ok,total_test_time=mytotal_test_time,test_date=mytest_date,test_done=1)

            output= '<h1>Thanks. The test has been recorded!</h1>'

            ########################################
            ## Checking if the generation is complete:

            # getting the chromosome:
            last_chromosome_modif = Chromosome.objects.get(id=mychromosome_id)
            last_creature = last_chromosome_modif.creature_id
            current_generation = last_chromosome_modif.generation
            ##output = output +" <h1>CREATURE_id -----> "+str(last_creature)+"</h1>"
            ##output = output +" <h1>CURRENT GENERATION -----> "+str(current_generation)+"</h1>"

            # Checking if creature is over
            if current_generation < generation_x_creature:

                # counting the number of chromosomes not done for the creature id and highest generation
                number_chromosomes = Chromosome.objects.filter(creature_id=last_creature, generation=current_generation).count()
                cursor = connection.cursor()
                cursor.execute("SELECT COUNT(  `genview_chromosome`.id ) FROM snag.`genview_chromosome` INNER JOIN snag.`genview_tasks` ON  `genview_chromosome`.`id` =  `genview_tasks`.`chromosome_id_id` WHERE  `genview_chromosome`.`creature_id_id` =%s AND  `genview_tasks`.`test_done` =1 AND `genview_chromosome`.`generation`=%s ", [last_creature, current_generation])
                total_rows = cursor.fetchone()
                ##output = output +" <h1>NUMBER CHROMOSOMES -----> "+str(number_chromosomes)+"</h1>"
                if int(list(total_rows)[0]) >= int(config("CHROMOSOMES_X_GENERATION")):
                    ## Call to genetics(last_creature, current_generation)
                    genetics(last_creature, current_generation)
                    ##output = output +" <h1>GENERATION FINISHED!! NEEDS REPRODUCTION <br />-----> "+str(config("CHROMOSOMES_X_GENERATION"))+"</h1>"
                else:
                    ##output = output +" <h1>GENERATION NOT FINISHED -----> "+str(config("CHROMOSOMES_X_GENERATION"))+" | len chromosomes ="+str(int(list(total_rows)[0]))+"<br /> REMAINS = "+str(int(config("CHROMOSOMES_X_GENERATION")) -  int(list(total_rows)[0]))+" </h1>"
                    pass
            else:
                output = output +"<h1>This creature is over; it reached the maximum number of generetion ( <b>"+str(generation_x_creature)+"</b> )</h1>"

        else:
            output = "<h1>Sorry, there is no more tests assigned to you or this page cannot be accessed directly!</h1>"
        output = output+"<h2>... you will be redirected to the user page in 4 seconds...</h2>"
        template = 'endtest.html'
        username = request.user.username

    return render_to_response(template, {'username': username,'output': output } )

#######################################################
def starttest(request):
    """
    This function build a webpage for the test.
    It gets the test id as chromosome id from GET cid's variable (p.e.: /?cid=123)
    """
    # vars:
    output = ''
    template = ''
    username = ''
    userid = ''
    questionTest = ''
    answersTest = ''
    idQuestion = ''
    chromosome_id = ''
    genId = ''
    data1 = []
    time_test_max = ''

    #First, check if user is autetificated:
    if not request.user.is_authenticated():
        output = "<h1>You need to login before to take a test!</h1>"
        template = 'home.html'
    else:
        template = 'starttest.html'
        username = request.user.username
        userid = request.user.id
        data = []
        data1 = []

        # getting config var:
        time_test_max = config("TIME_TEST_MAX")

        # DEBUG var:
        # data=['0127', '010132', '01010125', '01010219', '01010320', '010216', '01020117', '01020204', '01020329', '010321', '01030110', '01030215', '01030308', '0213', '020133', '02010118', '02010223', '02010301', '020234', '02020138', '02020228', '02020307', '020305', '02030109', '02030211', '02030331', '0324', '030136', '03010130', '03010202', '03010306', '030214', '03020139', '03020237', '03020312', '030303', '03030122', '03030226', '03030335']

        # Checking for available test for this user. In case there are some waiting, give the first one. Else, give no test

        if request.GET.get('cid'):
            myTasks = Tasks.objects.filter(chromosome_id=request.GET.get('cid'), test_done=0)
            out = '<h1>Sorry, this test is already done by user, <b>'+username+'</b></h1>'
        else:
            ##### Checking for available tests in Tasks table, and then get the data from Chromosome table
            myTasks = Tasks.objects.filter(user_id=userid, test_done='0')
            out = '<h1>Sorry, there are no test available for the user, <b>'+username+'</b></h1><p>Please contact SNAG team.</p>'
            # Id not available tasks for the user, leave:
        if len(myTasks)<1:
            output = out
            template = 'endtest.html'
            return render_to_response(template, {'username': username,'output': output})

        # Pending tasks for the user:
        tasksPending = []
        for t in myTasks:
            tasksPending.append(t.chromosome_id)
        chromosome_id = myTasks[0].chromosome_id_id
        userChromosome = Chromosome.objects.filter(id=chromosome_id)
        for u in userChromosome:
            data1 = u.data
        data = eval(data1)
        if len(data)==0:
            return render_to_response('home.html')

        #######################
        # Choosing random question / answer
        tags = {1:"Acceso remoto (desde fuera de la universidad)", 2:"Archivo general", 3:"Archivo hist&oacute;rico", 4:"Archivos", 5:"Autenticaci&oacute;n en los servicios en l&iacute;nea", 6:"Bibliograf&iacute;as", 7:"Bibliograf&iacute;as por asignaturas", 8:"Bibliograf&iacute;as por materias", 9:"Bibliograf&iacute;as por titulaciones", 10:"Carn&eacute; de usuario", 11:"Colecci&oacute;n de libros electr&oacute;nicos", 12:"Colecciones", 13:"Derechos de autor", 14:"Fondo antiguo", 15:"Formaci&oacute;n", 16:"Formaci&oacute;n a medida", 17:"Formaci&oacute;n en l&iacute;nea", 18:"Gu&iacute;as", 19:"Gu&iacute;as por materias", 20:"Gu&iacute;as tem&aacute;ticas", 21:"Internet", 22:"Legislaci&oacute;n y jurisprudencia", 23:"Libros", 24:"Multimedia", 25:"Normativa de pr&eacute;stamo", 26:"Nuevas adquisiciones", 27:"Organismos de normalizaci&oacute;n", 28:"Partituras y grabaciones sonoras", 29:"Patentes", 30:"Pel&iacute;culas", 31:"Pr&eacute;stamo", 32:"Pr&eacute;stamo interbibliotecario", 33:"Recursos electr&oacute;nicos", 34:"Revistas", 35:"Revistas electr&oacute;nicas", 36:"Revistas impresas", 37:"Servicios", 38:"Talleres formativos", 39:"Zona Wi-Fi y Eduroam"}
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
        idRamdom = randint(1, 118)
        answers = []
        questions = []
        questions.append("")
        answers.append("")
        for x in Contents.objects.all():
            questions.append(smart_str(x.question))
            answers.append(smart_str(x.answer))

        questionTest = questions[idRamdom]
        answersTest = answers[idRamdom]
        idQuestion = idRamdom%3
        if idQuestion==0:
            idQuestion=3
        genId = int(math.ceil(float(idRamdom)/float(3)))
        if genId<10:
            genId = "0"+str(genId) ## For example: genId = 3, needs to be genId = "03"
        genId = str(genId)

        output = ""
        mytree = dict()
        for allele in data:
            # prefix -> position
            pre = allele[:(len(allele)-2)]
            # sufix -> id
            suf = allele[(len(allele)-2):len(allele)]
            mytree[suf] = pre


        # frist nav bar
        first = []
        nav1 = "<div id='nav1'><p>"
        con = "<div id='hiddencontents'>"
        # We need to reorder de values, like 01xx, 02yy, 03zz
        mytree_sortedByValues = sorted(mytree.iteritems(), key=operator.itemgetter(1))
        for  k in mytree_sortedByValues:
            knum = int(k[0])
            if len(k[1]) == 2:
                nav1 = nav1+"\n\t<span id='"+str(k[0])+"-"+k[1]+"' class='first'>"+str(tags[knum])+"</span>"
                infos = ""
                c = 1
                for i in contents[knum].split("</li><li>"):
                    button = "&nbsp;<input type='image' src='"+MEDIA_URL+"/button.png' class='b' size='10' value='"+str(k[0])+"-"+str(c)+"'>"
                    infos = infos+"<li>"+i+button+"</li>"
                    c = c+1
                con = con+"\n\t<div id='c-"+str(k[0])+"-"+k[1]+"'>"+infos[4:]+"</div>"
                first.append(k[1])

        nav1 = nav1+"\n</p></div>"
        output = output+nav1

        # second nav bar
        second = []
        nav2 = "<div id ='nav2'><ul>"
        for f in first:
            for  k in mytree_sortedByValues:
                knum = int(k[0])
                if f == k[1][0:len(f)] and len(k[1]) == 4:
                    nav2 = nav2+"\n\t<li id='"+str(k[0])+"-"+k[1]+"' class='"+str(f)+" second'>"+str(tags[knum])+"</li>"
                    infos = ""
                    c = 1
                    for i in contents[knum].split("</li><li>"):
                        button = "&nbsp;<input type='image' src='"+MEDIA_URL+"/button.png' class='b' size='10' value='"+str(k[0])+"-"+str(c)+"'>"
                        if i[:4] == "<li>":
                            i = i[4:]
                        if i[-5:] == "</li>":
                            i = i[:-5]
                        infos = infos+"<li>"+i+button+"</li>"
                        c = c+1
                    con = con+"\n\t<div id='c-"+str(k[0])+"-"+k[1]+"'>"+infos+"</div>"
                    second.append(k[1])

        nav2 = nav2+"\n</ul></div>\n"
        output = output+nav2

        # third nav bar
        third = []
        nav3 = "<div id ='nav3'><ul>"
        for f in second:
            for  k in mytree_sortedByValues:
                knum = int(k[0])
                if f == k[1][0:len(f)] and len(k[1]) == 6:
                    nav3 = nav3+"\n\t<li id='"+str(k[0])+"-"+k[1]+"' class='"+str(f)+" third'>"+str(tags[knum])+"</li>"
                    infos = ""
                    c = 1
                    for i in contents[knum].split("</li><li>"):
                        button = "&nbsp;<input type='image' src='"+MEDIA_URL+"/button.png' class='b' size='10' value='"+str(k[0])+"-"+str(c)+"'>"
                        if i[:4] == "<li>":
                            i = i[4:]
                        if i[-5:] == "</li>":
                            i = i[:-5]
                        infos = infos+"<li>"+i+button+"</li>"
                        c = c+1
                    con = con+"\n\t<div id='c-"+str(k[0])+"-"+k[1]+"'>"+infos+"</div>"
                    third.append(k[1])

        nav3 = nav3+"\n</ul></div>\n"
        #nav3 = nav3+"<div id='contents'><ul></ul></div>\n"
        #con = con+"\n</div>\n"
        output = output+nav3

        # fourth nav bar
        #fourth = []
        nav4 = "<div id ='nav4'><ul>"
        for f in third:
            for  k in mytree.keys():
                knum = int(k)
                if f == mytree[k][0:len(f)] and len(mytree[k]) == 8:
                    nav4 = nav4+"\n\t<li id='"+str(k)+"-"+mytree[k]+"' class='"+str(f)+" fourth'>"+str(tags[knum])+"</li>"
                    infos = ""
                    c = 1
                    for i in contents[knum].split("</li><li>"):
                        button = "&nbsp;<input type='image' src='"+MEDIA_URL+"/button.png' class='b' size='10' value='"+str(k)+"-"+str(c)+"'>"
                        if i[:4] == "<li>":
                            i = i[4:]
                        if i[-5:] == "</li>":
                            i = i[:-5]
                        infos = infos+"<li>"+i+button+"</li>"
                        c = c+1
                    con = con+"\n\t<div id='c-"+str(k)+"-"+mytree[k]+"'>"+infos+"</div>"
                    #fourth.append(mytree[k])

        nav4 = nav4+"\n</ul></div>\n"
        nav4 = nav4+"<div id='contents'><ul></ul></div>\n"
        con = con+"\n</div>\n"
        output = output+nav4+con

    return render_to_response(template, {'data1':data1, 'username': username,'userid': userid,'questionTest': questionTest,'answersTest':answersTest,'idQuestion':idQuestion,'chromosome_id':chromosome_id, 'genId': genId,'output': output, 'TIME_TEST_MAX': time_test_max})

#######################################################
def profile(request):

    if request.user.is_authenticated():
        auth = "<p>User profile.</p>"
        auth += "<p>Hello {{ user.username }}. User is authenticated</p>"
    else:
        auth = "<p>User is anonymous</p>"

    return render_to_response('profile.html', {'auth': auth })