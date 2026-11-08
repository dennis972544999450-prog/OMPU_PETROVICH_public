# check <V,TV> = (1/12)[d0 + (2/pi) int_0^inf (Re P(i eta))^2/(eta^2 (1-phi(eta))) d eta], Re P(i eta) = 1 - E cos(eta H)
import numpy as np
from scipy.integrate import quad
src=open('grid_check.py').read().split('res={}')[0]; ns={}; exec(src,ns); solve=ns['solve']
h=0.0025; x,V,w=solve(h,12.0); m=x<1; xm=x[m]
Kt=np.clip(1-xm[:,None]-xm[None,:],0,None)*h
tail=(Kt@V[m])*np.sqrt(12)       # P(H>u)
d0=0.227350780091995
def RP(e): return np.sum((np.cos(e*(xm-h/2))-np.cos(e*(xm+h/2)))*tail)   # cellwise exact sin integral
def omp(e):
    if e<1e-2: e2=e*e; return e2/12-e2*e2/360
    s=np.sin(e/2)/(e/2); return 1-s*s
f=lambda e: RP(e)**2/(e*e*omp(e))
tot=0.0
edges=[1e-9]+[2*np.pi*k for k in range(1,400)]
for a,b in zip(edges[:-1],edges[1:]):
    v,_=quad(f,a,b,limit=200); tot+=v
B=edges[-1]
# tail: Re P -> 1 - E cos(eH) ~ 1 (oscillating part small), 1-phi ~ 1: integrand ~ 1/e^2 * (1 + osc)
tot+=1/B
print('formula <V,TV> = %.9f   residue/grid 0.039958599729'%((d0+(2/np.pi)*tot)/12))
