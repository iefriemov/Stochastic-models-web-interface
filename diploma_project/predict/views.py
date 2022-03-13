from django.shortcuts import render
from .forms import InputForm
from .predict_models.compute import compute
from .predict_models.Vasicek import vasicek
import os

def home(request):
    return render(request, 'predict/home.html')

def index(request):
    os.chdir(os.path.dirname(__file__))
    result = None
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            form2 = form.save(commit=False)
            result = compute(*vasicek(form2.A, form2.b, form2.w, form2.T))
            result = result.replace('static/', '')
    else:
        form = InputForm()

    return render(request, 'predict/model1.html',
            {'form': form,
             'result': result,
             })