import numpy as np
import math

def vasicek(K, theta, rates, sigma, dt):
    return K*(theta-rates)*dt + sigma*np.random.normal()
    
def cir(K, theta, rates, sigma, dt):
    return K*(theta-rates)*dt + sigma*math.sqrt(rates)*np.random.normal()

def rendleman_bartter(K, theta, rates, sigma, dt):
    return K*(theta-rates)*dt + sigma*rates*np.random.normal() 
    
def general_model(r0, K, theta, sigma, model, T=1., N=10, to_display=[], iter=50, for_mean=[]):
    print("general_model")
    if iter != 0:
        iter -= 1
        dt = T/float(N)
        rates = [r0]
        for _ in range(N):
            dr = model(K, theta, rates[-1], sigma, dt) 
            rates.append(rates[-1] + dr)
        to_display.append(rates)
        for_mean.append(rates[-1])
        return general_model(r0, K, theta, sigma, model, T, N, to_display, iter, for_mean)
    else:
        return range(N+1), to_display
