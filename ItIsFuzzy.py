import scipy.integrate as integrate
import numpy as np

EVENT_SCALING = 15
EVENT_THRESHOLD = 0.1

# Calculate the integral of the sigmoid function we are using
# for event detection
# We can use this during centroid calculations
def event_fuzzy_integral(a, b):
    return integrate.quad(lambda x: 1/(1 + np.exp(-EVENT_SCALING * (x - EVENT_THRESHOLD))), a, b)

def event_constant_integral(a, b, height):
    return height * (b-a)
