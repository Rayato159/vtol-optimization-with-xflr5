import numpy as np

def range(eff, V, C, Cd):
    A = eff*V*C
    B = (1/np.sqrt(1.2148*1.2))*(Cd**(1/4))*(2*9.81*14*(np.sqrt(0.0525)**(3/2)))
    C = (1**0.3)*((A/B)**1.3)
    D = np.sqrt(((2*9.81*14)/(1.2148*1.2))*np.sqrt(0.0525/Cd))
    E = C*D*3.6
    return E

R = range(0.5, 11.1, 3.5, 0.017)
print(R)