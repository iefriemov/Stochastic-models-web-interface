from .compute import compute, estimate_parameters
from .stoch_models import general_model, vasicek, cir , rendleman_bartter

#it's pity that there is not case switch in this python version 
def selected_model(param, choose, exising_data = None):
    choose = int(choose)
    if choose == 1:
        print('in 1')
        return compute(general_model(*param, model=vasicek), exising_data)
    elif choose == 2:
        return compute(general_model(*param, model=cir), exising_data)
    elif choose == 3:
        return compute(general_model(*param, model=rendleman_bartter), exising_data)