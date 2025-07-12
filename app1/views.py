from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.



def index(request):
    return HttpResponse("<p>This is initialization of Project.</p>")


def about(request):
    return HttpResponse("<p>This is initialization of Project.</p>")


def home(request):
    return render(request, 'index.html')