from django.shortcuts import render, redirect
from .models import KpiModel, SportModel, EvrikaModel, BookModel, WorkModel
from django.shortcuts import get_object_or_404
from decimal import Decimal
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


def SignupPage(request):
    return render(request, 'signup.html')


def LoginPage(request):
    return render(request, 'login.html')


def book(request, id=None):
    kpi = get_object_or_404(KpiModel, id=id)
    books = BookModel.objects.filter(kpi=kpi)
    return render(request, 'book.html', {"books":books, "kpi":kpi})



def sport(request, id=None):
    kpi = get_object_or_404(KpiModel, id=id)
    sports = SportModel.objects.filter(kpi=kpi)
    return render(request, 'sport.html', {"sports":sports, 'kpi':kpi})
    # else:
    #     details = request.POST.get('details', '')
    #     score = request.POST.get('score', '')
    #     kpi_id = request.POST.get('kpi')
    #     kpi = KpiModel.objects.get(id=kpi_id)
    #     sport = SportModel.objects.create(kpi=kpi, details=details, score=score)
    #     sport.save()
    #     return redirect('sport')
    


def work(request, id=None):
    kpi = get_object_or_404(KpiModel, id=id)
    works = WorkModel.objects.filter(kpi=kpi).order_by("deadline")
    if request.method == 'POST':
        #  edit the existing work
        kpi = KpiModel.objects.get(id=id)
        work_id = request.POST.get('work_id')
        if work_id is not None:
            work = WorkModel.objects.get(id=work_id)
            deadline = request.POST.get('deadline')
            score = request.POST.get('score')
            description = request.POST.get('description', '')
            work.deadline = deadline
            work.score = score
            work.description = description
            work.save()

        #  new work creation
        else:
            n_deadline = request.POST.get('n_deadline')    
            n_score = request.POST.get('n_score', )
            n_description = request.POST.get('n_description', '')
            
            n_work = WorkModel(deadline=n_deadline, score=n_score, description=n_description, kpi=kpi)
            n_work.save()
        return redirect('/')
    
    elif request.method == 'DELETE':
        work_id = request.POST.get('work_id')
        obj = get_object_or_404(WorkModel, id=work_id)
        obj.delete()
        return redirect('/')
    return render(request, 'work.html', {"works":works, 'kpi':kpi})


def eureka(request, id=None):
    kpi = get_object_or_404(KpiModel, id=id)
    evrikas = EvrikaModel.objects.filter(kpi=kpi)
    return render(request, 'eureka.html', {"evrikas":evrikas, 'kpi':kpi})


def reminder(request):
    return render(request, 'reminder.html')


