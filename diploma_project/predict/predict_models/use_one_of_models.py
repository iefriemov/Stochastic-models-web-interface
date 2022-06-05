from .compute import compute, estimate_parameters
from .stoch_models import vasicek, cir, rendleman_bartter           

#it's pity that there is not case switch in this python version 
def selected_model(param, choose, exising_data = None):
    if choose == 1:
        result = compute(vasicek(*param), exising_data)
    elif choose == 2:
        result = compute(cir(*param), exising_data)
    else:
        result = compute(rendleman_bartter(*param), exising_data)
        
    return result
