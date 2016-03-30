import numpy as np

# Compute fuzzy scores of the certainty

def compute_certainty(event_fuzz, cred_fuzz):
    points = np.linspace(0.0, 1.0, num=51, endpoint=True)
    # Rule 1: HE AND HC -> HCERT
    high_cap = min(event_fuzz, cred_fuzz)
    # Rule 2: LE AND HC -> MCERT
    # Rule 3: HE AND LC -> MCERT
    mid_cap = max(min(1-event_fuzz, cred_fuzz), min(event_fuzz, 1-cred_fuzz))
    # Rule 4: LE AND LC -> LCERT
    low_cap = min(1-event_fuzz, 1-cred_fuzz)
    # Get the value for each point
    cred_points = [get_certainty_point(x, low_cap, mid_cap, high_cap) for x in points]
    # Compute centroid of the points
    weightsum = 0
    midsum = 0
    for i in range(1, 51):
        midpoint = (points[i-1] + points[i])/2.0
        distance = points[i] - points[i-1]
        sq_area = (distance)*min(cred_points[i], cred_points[i-1])
        tri_area = abs(cred_points[i] - cred_points[i-1])*distance/2.0
        area = sq_area + tri_area
        weightsum += area
        midsum += area * midpoint
    return midsum / weightsum

def get_certainty_point(x, low_cap, mid_cap, high_cap):
    return max(get_low_certainty(x, low_cap),
               get_mid_certainty(x, mid_cap),
               get_high_certainty(x, high_cap))

def get_low_certainty(x, cap):
    if x < 0.25:
        val = 1
    elif x < 0.5:
        val = -4*x + 2
    else:
        val = 0
    return min(val, cap)

def get_mid_certainty(x, cap):
    if x < 0.25:
        val = 0
    elif x < 0.5:
        val = 4*x - 1
    elif x < 0.75:
        val = -4*x + 3
    else:
        val = 0
    return min(val, cap)

def get_high_certainty(x, cap):
    if x < 0.5:
        val = 0
    elif x < 0.75:
        val = 4*x - 2
    else:
        val = 1
    return min(val, cap)
