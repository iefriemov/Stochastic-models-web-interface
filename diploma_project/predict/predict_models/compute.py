import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import os, time, glob

def compute(data, exising_data=None):
    """Return filename of plot of the damped_vibration function."""
    print(os.getcwd())
    plt.figure()  

    x, y = data
    y = np.mean(y, axis=0)
    mean_end_price = round(y[-1],2)
    
    if exising_data is not None:
        N = len(exising_data) 
        y[0] = exising_data[-1]
        N -=1
        plt.plot(np.arange(len(exising_data)), exising_data) 
        
    else:
        N = 0

    plt.plot(list(map(lambda x: x + N, x)), y) 
    plt.suptitle(f"среднее значение:{mean_end_price}", fontweight='bold')
        
        
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


def estimate_parameters(sigma_t):
    # define regression specification
    sigma_sqrt = np.sqrt(sigma_t[:-1])
    y = np.diff(sigma_t) / sigma_sqrt
    x1 = 1.0 / sigma_sqrt
    x2 = sigma_sqrt
    X = np.concatenate([x1.reshape(-1, 1), x2.reshape(-1, 1)], axis=1)
    # regression model
    reg = LinearRegression(fit_intercept=False)
    reg.fit(X, y)
    # regression coefficients
    ab = reg.coef_[0]
    a = -reg.coef_[1]
    b = ab / a
    # residuals and their standard deviation
    y_hat = reg.predict(X)
    c = np.std(y - y_hat)
    r0 = sigma_t[len(sigma_t)-1]
    return r0, a, b, c

if __name__ == '__main__':
    print(compute(1, 0.1, 1, 20))
