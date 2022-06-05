import numpy as np
import math

def vasicek(r0, K, theta, sigma, T=1., N=10, to_display=[], iter=50, for_mean=[]):
    if iter != 0:
        iter -= 1
        dt = T/float(N)
        rates = [r0]
        for _ in range(N):
            dr = K*(theta-rates[-1])*dt + sigma*np.random.normal()
            rates.append(rates[-1] + dr)
        to_display.append((range(N+1), rates))
        for_mean.append(rates[-1])
        return vasicek(r0, K, theta, sigma, T, N, to_display, iter, for_mean)
    else:
        return to_display

def cir(r0, K, theta, sigma, T=1.,N=10, to_display=[], iter=50):
    if iter != 0:
        iter -= 1
        dt = T/float(N)
        rates = [r0]
        for _ in range(N):
            dr = K*(theta-rates[-1])*dt + sigma*math.sqrt(rates[-1])*np.random.normal()
            rates.append(rates[-1] + dr)
        to_display.append((range(N+1), rates))
        return rendleman_bartter(r0, K, theta, sigma, T, N, to_display, iter)
    else:
        return to_display

def rendleman_bartter(r0, K, theta, sigma, T=1., N=10, to_display=[], iter=50): # The Brennan and Schwartz model
    if iter != 0:
        iter -= 1
        dt = T/float(N)
        rates = [r0]
        for _ in range(N):
            dr = K*(theta-rates[-1])*dt + sigma*rates[-1]*np.random.normal()
            rates.append(rates[-1] + dr)
        to_display.append((range(N+1), rates))
        return rendleman_bartter(r0, K, theta, sigma, T, N, to_display, iter)
    else:
        return to_display

if __name__ == '__main__':
    print(vasicek(0.01875, 0.20, 0.01, 0.012, 10., 200))