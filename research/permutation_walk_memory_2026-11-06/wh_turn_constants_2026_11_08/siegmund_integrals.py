# b1, b3 with cancellation-free series near 0; compare P_min and E[H^5] with grid
import numpy as np
from math import factorial
from scipy.integrate import quad
CUT=1.0
def v_of(e):   # u/e^2 where u = 12(1-phi)/e^2 - 1
    return sum(24*(-1)**i*e**(2*i-2)/factorial(2*i+4) for i in range(1,14))
def L(e):
    if e<CUT: return np.log1p(v_of(e)*e*e)
    s=np.sin(e/2)/(e/2); return np.log(12*(1-s*s)/(e*e))
def f1(e):
    return L(e)/(e*e) if e>0 else -1/30
def f3(e):
    if e<CUT:
        v=v_of(e)
        a=sum(24*(-1)**i*e**(2*i-4)/factorial(2*i+4) for i in range(2,14))
        b=sum((-1)**(n+1)*v**n*e**(2*n-4)/n for n in range(2,14))
        return a+b
    return (L(e)/(e*e)+1/30)/(e*e)
def integ(fun, nk=4000):
    tot=0.0
    edges=[0,CUT]+[2*np.pi*k for k in range(1,nk+1)]
    for a,b in zip(edges[:-1],edges[1:]):
        v,_=quad(fun,a,b,limit=400,epsabs=1e-17,epsrel=1e-13); tot+=v
    return tot, edges[-1]
t1,B=integ(f1); t1+=(np.log(12/B**2)-2)/B - 2/(3*B**3)
t3,B=integ(f3); t3+=(3*np.log(12/B**2)-2)/(9*B**3)+1/(30*B)
b1=t1/np.pi; b3=-t3/np.pi; b2=1/60; b4=1/50400
d0=-b1
a1=b1; a2=b2+b1**2/2; a3=b3+b1*b2+b1**3/6; a4=b4+b1*b3+b2**2/2+b1**2*b2/2+b1**4/24
EH=1/np.sqrt(12)
print('delta0=%.15f  b3=%.15f'%(d0,b3))
print('EH^k:', ['%.12f'%(EH*(-1)**(k-1)*factorial(k)*c) for k,c in zip(range(2,6),[a1,a2,a3,a4])])
pmax=0.5+a1+a2; pmin=(1/8-d0/6+a4)/pmax
print('P_max=%.13f P_min=%.13f'%(pmax,pmin))
