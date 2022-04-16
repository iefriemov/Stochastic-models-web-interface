from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import InputForm
from .predict_models.compute import compute, parameters
from .predict_models.Vasicek import vasicek
import pandas as pd
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
        result = compute(*vasicek(*parameters(df.iloc[:,0].to_numpy())))
        result = result.replace('static/', '')
        return render(request, 'predict/from_csv.html',
                {
                    'result': result,
                })
    except Exception as e:
        messages.error(request,"Unable to upload CVS file. " + repr(e))

