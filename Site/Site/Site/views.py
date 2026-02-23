from tempfile import template

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.template import  loader
from django.urls import reverse_lazy


#def home(request):
#    template = loader.get_template('site/site.html')
#    return render(request, 'site/site.html')
#     return HttpResponse (template.render (context, request))

