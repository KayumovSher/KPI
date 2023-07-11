from django.shortcuts import render, redirect
from .models import KpiModel, SportModel, EvrikaModel, BookModel, WorkModel
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
    kpi_models = KpiModel.objects.all()
    return render(request, 'book.html', {"books":books, "kpi_models":kpi_models})


def sport(request):
    if request.method == 'GET':
        sports = SportModel.objects.all()
        kpi_models = KpiModel.objects.all()

    else:
        details = request.POST.get('details')
        score = request.POST.get('score')
        kpi_id = request.POST.get('kpi')
        kpi = KpiModel.objects.get(id=kpi_id)
        sport = SportModel.objects.create(kpi=kpi, details=details, score=score)
        sport.save()
        return redirect('sport')
    return render(request, 'sport.html', {"sports":sports, 'kpi_models':kpi_models})
    

def work(request):
    works = WorkModel.objects.all().order_by("deadline")
    kpi_models = KpiModel.objects.all()
    return render(request, 'work.html', {"works":works, 'kpi_models':kpi_models})

    # id = 1
    # kpi = KpiModel.objects.get(id=id)
    # score = request.data.GET("score")
    # deadline = request.data.GET("deadline")
    # work = WorkModel.objects.create(score=score, deadline=deadline, kpi=kpi)
    # work.save()
    # works = WorkModel.objects.all()


def eureka(request):
    evrikas = EvrikaModel.objects.all()
    kpi_models = KpiModel.objects.all()
    return render(request, 'eureka.html', {"evrikas":evrikas, 'kpi_models':kpi_models})


def reminder(request):
    return render(request, 'reminder.html')


