from django.shortcuts import render
from .models import KpiModel

# Create your views here.

def index(request):
    kpi_models = KpiModel.objects.all()
    return render(request, 'index.html', {"kpi":kpi_models})


def book(request):
    kpi_models = KpiModel.objects.all()
    return render(request, 'book.html', {"kpi":kpi_models})


def sport(request):
    return render(request, 'sport.html')


def work(request):
    kpi_models = KpiModel.objects.all()
    return render(request, 'work.html', {"kpi":kpi_models})


def eureka(request):
    kpi_models = KpiModel.objects.all()
    return render(request, 'eureka.html', {"kpi":kpi_models})
