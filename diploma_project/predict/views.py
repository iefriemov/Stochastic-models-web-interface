from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import ModelForm
from .predict_models.compute import estimate_parameters
from .predict_models.use_one_of_models import selected_model
import pandas as pd
import os
from .predict_models.connect_posetgres import get_interest


def home(request):
    return render(request, 'predict/home.html')

def models_predict(request):
    return render(request, 'predict/models_predict.html')

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
        
        choose = request.POST["my_options"] 
        df = pd.read_csv(csv_file)
        input_data = df.iloc[:,0].to_numpy()
        parameters = estimate_parameters(input_data)
        result = selected_model(parameters, choose, input_data)
        result = result.replace('static/', '')
        return render(request, 'predict/from_csv.html',
                {
                    'result': result,
                    'r0' : parameters[0],
                    'a' : parameters[1],
                    'b' : parameters[2],
                    'c' : parameters[3],
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
            
            choose = form2.status
            param = [form2.A, form2.b, form2.w, form2.T]
            
            result = selected_model(param, int(choose))
            result = result.replace('static/', '')
    else:
        form = ModelForm()

    return render(request, 'predict/stoch_model.html',
            {'form': form,
            'result': result,
            })
    
    
def interests(request):
    if "GET" == request.method:
        return render(request, "predict/interests.html")
    # if not GET, then proceed with processing
    try:
        input_data = get_interest()
        #data = data[data != None]
        choose = request.POST["my_options"]
        #input_data = np.asarray(data)
        input_data = pd.DataFrame(input_data).dropna()
        input_data = input_data.iloc[:,0].to_numpy()
        #print(input_data)
        parameters = estimate_parameters(input_data)
        #print(parameters)
        #print(parameters, choose, input_data)
        result = selected_model(parameters, int(choose), input_data)
        print(result)
        result = result.replace('static/', '')
        return render(request, 'predict/interests.html',
                {
                    'result': result,
                    'r0' : parameters[0],
                    'a' : parameters[1],
                    'b' : parameters[2],
                    'c' : parameters[3],
                })
    except Exception as e:
        messages.error(request,"Unable to upload CVS file. " + repr(e))