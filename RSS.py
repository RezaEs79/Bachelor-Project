# Declare variables and compute RSS
# Part 1: Computations independant of the random variable
# for shadow fading
import math
import numpy as np
from numpy import random
def CalcRSS(distance):
    # distance = 200
    g = 150
    Pt = 20
    Po = 38
    grad1 = 2
    grad2 = 2
    alpha = math.exp(-1/85)
    sigma1 = math.sqrt(8)
    sigma2 = math.sqrt(sigma1**2 * (1 - alpha**2))
    # Path Loss
    RSS01 = Pt - Po - (10 * grad1 * math.log10(distance) +
                    10 * grad2 * math.log10(distance/g))
    #  Part 2: Adding the random variable for shadow fading
    # s(d) = is the correlated log normal fading
    s1 = sigma1 * random.normal()
    s2 = alpha * s1 + sigma2 * random.normal()
    RSS1 = RSS01 + s2
    return RSS1
