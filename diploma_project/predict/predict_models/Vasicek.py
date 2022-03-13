import numpy as np

def vasicek(r0, K, theta, sigma, T=1., N=12):
    dt = T/float(N)
    rates = [r0]
    for i in range(N):
        dr = K*(theta-rates[-1])*dt + sigma*np.random.normal()
        rates.append(rates[-1] + dr)
        
    return range(N+1), rates 

if __name__ == '__main__':
    print(vasicek(0.01875, 0.20, 0.01, 0.012, 10., 200))