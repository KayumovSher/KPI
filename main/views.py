from django.shortcuts import render
from .models import KpiModel, SportModel, EvrikaModel, BookModel, WorkModel
# Create your views here.
def index(request):
    return render(request, 'index.html')





