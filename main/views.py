from django.shortcuts import render
from .models import KpiModel

# Create your views here.
def index(request):
    kpi_models = KpiModel.objects.all()
    return render(request, 'index.html', {"kpi":kpi_models})
