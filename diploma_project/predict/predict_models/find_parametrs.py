import numpy as np 

# Maximum Likelihood Estimation to calibrate parameters
def find_parameters(rates, dt=1/252):
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
  return [r0, kappa, theta, sigma]