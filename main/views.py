from django.shortcuts import render
from .models import KpiModel, SportModel, EvrikaModel, BookModel, WorkModel
from .models import KpiModel
# Create your views here.

def index(request):
    kpi_models = KpiModel.objects.all()
    kpi_array = [x for x in kpi_models]
    books = sum(x.score for x in BookModel.objects.filter(kpi__in=kpi_array))
    sports = sum(x.score for x in SportModel.objects.filter(kpi__in=kpi_array))
    evrikas = sum(x.score for x in EvrikaModel.objects.filter(kpi__in=kpi_array))
    works = sum(x.score for x in WorkModel.objects.filter(kpi__in=kpi_array))
    context = {"kpi":kpi_models, "books":books, "sports":sports, "evrikas":evrikas, "works":works}
    return render(request, 'index.html', context)

def book(request):
    books = BookModel.objects.all()
    return render(request, 'book.html', {"books":books})


def sport(request):
    sports = SportModel.objects.all()
    return render(request, 'sport.html', {"sports":sports})


def work(request):
    works = WorkModel.objects.all()
    return render(request, 'work.html', {"works":works})


def eureka(request):
    evrikas = EvrikaModel.objects.all()
    return render(request, 'eureka.html', {"evrikas":evrikas})


