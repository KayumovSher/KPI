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


class WorkViews:
    def edit_work(self, request, kpi_id, work_id):
        # Retrieve the necessary objects
        kpi = get_object_or_404(KpiModel, id=kpi_id)
        work = get_object_or_404(WorkModel, id=work_id)

        if request.method == 'POST':
            # Process the form data and update the work object
            deadline = request.POST.get('deadline')
            score = request.POST.get('score')
            description = request.POST.get('description', '')

            work.deadline = deadline
            work.score = score
            work.description = description
            work.save()

            return redirect('/')

        return render(request, 'edit_work.html', {'kpi': kpi, 'work': work})

    def delete_work(self, request, kpi_id, work_id):
        if request.method == 'POST':
            # Delete the work object
            work = get_object_or_404(WorkModel, id=work_id)
            work.delete()

        return redirect('/')

    def create_work(self, request, kpi_id):
        kpi = get_object_or_404(KpiModel, id=kpi_id)

        if request.method == 'POST':
            # Process the form data and create a new work object
            deadline = request.POST.get('n_deadline')
            score = request.POST.get('n_score', '')
            description = request.POST.get('n_description', '')

            new_work = WorkModel(deadline=deadline, score=score, description=description, kpi=kpi)
            new_work.save()

            return redirect('/')

        return render(request, 'create_work.html', {'kpi': kpi})
    
    return render(request, 'work.html', {"works": works, 'kpi': kpi})

def eureka(request, id=None):
    kpi = get_object_or_404(KpiModel, id=id)
    evrikas = EvrikaModel.objects.filter(kpi=kpi)
    return render(request, 'eureka.html', {"evrikas":evrikas, 'kpi':kpi})


def reminder(request):
    return render(request, 'reminder.html')