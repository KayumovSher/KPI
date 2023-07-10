from django.shortcuts import render
from .models import KpiModel

# Create your views here.

def index(request):
    kpi_models = KpiModel.objects.all()
    return render(request, 'index.html', {"kpi":kpi_models})


def book(request):
    return render(request, 'book.html')


def sport(request):
    return render(request, 'sport.html')


def work(request):
    return render(request, 'work.html')


def eureka(request):
    return render(request, 'eureka.html')
