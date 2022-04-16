from numpy import exp, cos, linspace
import numpy as np
import matplotlib.pyplot as plt
import os, time, glob

def compute(x, y):
    """Return filename of plot of the damped_vibration function."""
    print(os.getcwd())
    plt.figure()  # needed to avoid adding curves in plot
    plt.plot(x, y)
    if not os.path.isdir('static'):
        os.mkdir('static')
    else:
        # Remove old plot files
        for filename in glob.glob(os.path.join('static', '*.png')):
            os.remove(filename)
    # Use time since Jan 1, 1970 in filename in order make
    # a unique filename that the browser has not chached
    plotfile = os.path.join('static', str(time.time()) + '.png')
    plt.savefig(plotfile)
    return plotfile

def parameters(rates, dt=1/252):
    n = len(rates)
    Ax = sum(rates[0:(n-1)])
    Ay = sum(rates[1:n])
    Axx = np.dot(rates[0:(n-1)], rates[0:(n-1)])
    Axy = np.dot(rates[0:(n-1)], rates[1:n])
    Ayy = np.dot(rates[1:n], rates[1:n])
    theta = (Ay * Axx - Ax * Axy) / (n * (Axx - Axy) - (Ax**2 - Ax*Ay))
    kappa = -np.log((Axy - theta * Ax - theta * Ay + n * theta**2) / (Axx - 2*theta*Ax + n*theta**2)) / dt
    a = np.exp(-kappa * dt)
    sigmah2 = (Ayy - 2*a*Axy + a**2 * Axx - 2*theta*(1-a)*(Ay - a*Ax) + n*theta**2 * (1-a)**2) / n
    sigma = np.sqrt(sigmah2*2*kappa / (1-a**2))
    r0 = rates[n-1]
    return r0, kappa, theta, sigma

if __name__ == '__main__':
    print(compute(1, 0.1, 1, 20))
