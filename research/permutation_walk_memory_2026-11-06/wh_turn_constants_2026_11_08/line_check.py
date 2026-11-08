import numpy as np
src=open('vtv_residue.py').read().split('# sanity')[0]; ns={}; exec(src,ns); logP=ns['logP']
def Q(s): return 1-4*np.sinh(s/2)**2/s**2
for c in [2.0,1.0]:
    taus=np.linspace(0,400,8001); vals=[]
    for t in taus:
        s=complex(c,t); P=np.exp(logP(s)); vals.append((Q(s)/(s*s*P*P)).real)
    vals=np.array(vals); I=np.trapezoid(vals,taus)
    # tail: Re(1/s^2) beyond tau_max: integral = -tau_m/(tau_m^2+c^2)
    tm=taus[-1]; I+= -tm/(tm*tm+c*c)
    print('c=%.1f  <V,TV> = %.9f'%(c, -I/(12*np.pi)))
