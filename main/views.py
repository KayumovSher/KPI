from django.shortcuts import render, redirect
from .models import KpiModel, SportModel, EvrikaModel, BookModel, WorkModel
from django.shortcuts import get_object_or_404
# Create your views here.

def index(request):
    kpi_models = KpiModel.objects.all()
    result = []
    for x in kpi_models:
        books = sum(x.score for x in BookModel.objects.filter(kpi=x))
        sports = sum(x.score for x in SportModel.objects.filter(kpi=x))
        evrikas = sum(x.score for x in EvrikaModel.objects.filter(kpi=x))
        works = sum(x.score for x in WorkModel.objects.filter(kpi=x))
        result.append({"kpi":x, "sports":sports, "evrikas":evrikas, "works":works, "books":books})
    
    return render(request, 'index.html', context={"results":result})

def book(request, id=None):
    kpi = get_object_or_404(KpiModel, id=id)
    books = BookModel.objects.filter(kpi=kpi)
    return render(request, 'book.html', {"books":books, "kpi":kpi})



def sport(request, id=None):
    kpi = get_object_or_404(KpiModel, id=id)
    sports = SportModel.objects.filter(kpi=kpi)
    return render(request, 'sport.html', {"sports":sports, 'kpi':kpi})
    # else:
    #     details = request.POST.get('details')
    #     score = request.POST.get('score')
    #     kpi_id = request.POST.get('kpi')
    #     kpi = KpiModel.objects.get(id=kpi_id)
    #     sport = SportModel.objects.create(kpi=kpi, details=details, score=score)
    #     sport.save()
    #     return redirect('sport')
    

def work(request, id=None):
    kpi = get_object_or_404(KpiModel, id=id)
    works = WorkModel.objects.filter(kpi=kpi).order_by("deadline")
    return render(request, 'work.html', {"works":works, 'kpi':kpi})

    # id = 1
    # kpi = KpiModel.objects.get(id=id)
    # score = request.data.GET("score")
    # deadline = request.data.GET("deadline")
    # work = WorkModel.objects.create(score=score, deadline=deadline, kpi=kpi)
    # work.save()
    # works = WorkModel.objects.all()


def eureka(request, id=None):
    kpi = get_object_or_404(KpiModel, id=id)
    evrikas = EvrikaModel.objects.filter(kpi=kpi)
    return render(request, 'eureka.html', {"evrikas":evrikas, 'kpi':kpi})


def reminder(request):
    return render(request, 'reminder.html')


