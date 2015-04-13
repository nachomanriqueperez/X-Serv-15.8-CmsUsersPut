from django.shortcuts import render
from models import PutApp
from django.conf.urls import patterns, include, url
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def contentapp(request,resourceName):
    response = '<h1> THIS IS THE WEB SITE </h1>' 
    if request.user.is_authenticated():
        logged = "<br><br>Logueado como: " + request.user.username +\
                "       <a href='/admin/logout/'>Deslogueate</a><br>"   
        if request.method == "GET":
            try:
                info = PutApp.objects.get(titulo=resourceName)
                return HttpResponse(response + info.contenido)
            except PutApp.DoesNotExist:
                response += '<body> El valor no existe, introduzcalo </body>'
                response += logged
                form = "<form action='' method='POST'>\n"
                form += "Titulo: <input type='text' name='titulo' value=''><br>\n"
                form += "Contenido: <input type='text' name='contenido'><br>\n"
                form += "<input type='submit' value='enviar'>\n"
                form += "</form>\n"
                response += form
                response += " <h2><a href='http://127.0.0.1:8000/admin/'>Pulse aqui para ver los datos</a></h2>"
                return HttpResponse(response)
        elif request.method == "PUT":
            response += '<body> Metemos en base de datos:  </body>' 
            (namePage, Page) = request.body.split(';')
            newPage = PutApp(titulo=namePage, contenido=Page)
            newPage.save()
            response += "Titulo: " + request.POST['titulo'] 
            response += ", Contenido: " + request.POST['contenido']
            return HttpResponse(response)
        elif request.method == "POST":
                response += '<body> Metemos en base de datos:  </body>' 
                newPage = PutApp(titulo=request.POST['titulo'], contenido=request.POST['contenido'])
                newPage.save()
                response += "TITULO: " + request.POST['titulo'] 
                response += ", CONTENIDO: " + request.POST['contenido']
                response += " <h2><a href='""'>Pulse aqui para ir a la url original</a></h2>"
                return HttpResponse(response)
        else:
                response += '<body> NO SENSE PAGE </body>'
                return HttpResponse(response)
    else:
        logged = "<br><br>No estas logueado <a href= '/admin/login/'>Logueate</a><br>"
        return HttpResponse(response + logged) 
