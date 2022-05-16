from lib2to3.pgen2.pgen import DFAState
from this import d
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import InputForm, ModelForm
from .predict_models.compute import compute, estimate_parameters
from .predict_models.stoch_models import vasicek, cir, rendleman_bartter
import pandas as pd
import os


def home(request):
    return render(request, 'predict/home.html')

def Vasicek_model(request):
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

    return render(request, 'predict/Vasicek_model.html',
            {'form': form,
             'result': result,
             })
    
def CIR_model(request):
    os.chdir(os.path.dirname(__file__))
    result = None
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            form2 = form.save(commit=False)
            result = compute(*cir(form2.A, form2.b, form2.w, form2.T))
            result = result.replace('static/', '')
    else:
        form = InputForm()

    return render(request, 'predict/CIR_model.html',
            {'form': form,
             'result': result,
             })

def Rendleman_Bartter_model(request):
    os.chdir(os.path.dirname(__file__))
    result = None
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            form2 = form.save(commit=False)
            result = compute(*rendleman_bartter(form2.A, form2.b, form2.w, form2.T))
            result = result.replace('static/', '')
    else:
        form = InputForm()

    return render(request, 'predict/Rendleman_Bartter_model.html',
            {'form': form,
             'result': result,
             })
  
def process_csv_file(request):
    if "GET" == request.method:
        return render(request, "predict/from_csv.html")
    # if not GET, then proceed with processing
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("predict-csv"))
        #if file is too large, return message
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("predict-csv"))
        
        df = pd.read_csv(csv_file)
        result = compute(*vasicek(*estimate_parameters(df.iloc[:,0].to_numpy())))
        result = result.replace('static/', '')
        return render(request, 'predict/from_csv.html',
                {
                    'result': result,
                })
    except Exception as e:
        messages.error(request,"Unable to upload CVS file. " + repr(e))
        
        
def stoch_model(request):
    os.chdir(os.path.dirname(__file__))
    result = None
    if request.method == 'POST':
        form = ModelForm(request.POST)
        if form.is_valid():
            form2 = form.save(commit=False)
            
            #it's pity that there is not case switch in this python version
            choose = form2.status
            
            if choose == 1:
                result = compute(*vasicek(form2.A, form2.b, form2.w, form2.T))
            elif choose == 2:
                result = compute(*cir(form2.A, form2.b, form2.w, form2.T))
            else:
                result = compute(*rendleman_bartter(form2.A, form2.b, form2.w, form2.T))
            result = result.replace('static/', '')
    else:
        form = ModelForm()

    return render(request, 'predict/stoch_model.html',
            {'form': form,
             'result': result,
             })
        

