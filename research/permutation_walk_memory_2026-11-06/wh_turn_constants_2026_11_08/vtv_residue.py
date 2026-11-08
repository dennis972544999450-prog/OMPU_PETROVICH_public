# <V,TV> = delta0/6 - (1/24) sum_{left roots s_k} P(-s_k)^2/(s_k - sinh s_k)
# P(s)=1-E e^{-sH} for Re s>0 from the Schwarz integral of log|P(i eta)|^2 = log(1-phi):
#   log P(s) = log(s/(s+1)) + (2s/pi) int_0^inf g(t)/(s^2+t^2) dt,  g=(1/2)log((1-phi)(1+t^2)/t^2)
# Fully independent of the grid; only phi(t)=sinc^2(t/2) is used.
import numpy as np, time
from math import factorial
t0=time.time()
NCH=6000; NG=64
xg,wg=np.polynomial.legendre.leggauss(NG)
edges=np.concatenate([[0.0,1.0],2*np.pi*np.arange(1,NCH+1)])
T=[];W=[]
for a,b in zip(edges[:-1],edges[1:]):
    T.append((b-a)/2*xg+(a+b)/2); W.append((b-a)/2*wg)
T=np.concatenate(T); W=np.concatenate(W); TMAX=edges[-1]
def g_of(t):
    out=np.empty_like(t)
    m=t<1.0
    tt=t[m]
    v=sum(24*(-1)**i*tt**(2*i)/factorial(2*i+4) for i in range(1,14))  # 12(1-phi)/t^2 - 1
    out[m]=0.5*(np.log1p(v)-np.log(12.0)+np.log1p(tt*tt))
    tt=t[~m]; s=np.sin(tt/2)/(tt/2)
    out[~m]=0.5*np.log((1-s*s)*(1+tt*tt)/(tt*tt))
    return out
G=g_of(T)*W
def logP(s):
    I=np.sum(G/(s*s+T*T))
    # tail t>TMAX: g ~ (-1/2 + cos t)/t^2 ; non-oscillating part: int (-1/2)/t^2 /(s^2+t^2) ~ -1/(6 TMAX^3)
    I+= -1/(6*TMAX**3)
    return np.log(s/(s+1))+(2*s/np.pi)*I
# sanity: P(s) at small real s ~ s/sqrt12 (1 - d0 s)
d0=0.227350780091995
for s in [1e-3,1e-2]:
    P=np.exp(logP(complex(s)))
    print('check P(%g)/(s E[H]) = %.10f vs 1-d0 s+(1/60+d0^2/2)s^2 = %.10f'%(s,(P/(s/np.sqrt(12))).real,1-d0*s+(1/60+d0*d0/2)*s*s))
J=1000000
j=np.arange(1,J+1); sig=np.where(j%2==0,1.0,-1.0)
a=(j+0.5)*np.pi; w=a+1j*np.arccosh(a)
for it in range(60):
    dw=(np.sin(w)-sig*w)/(np.cos(w)-sig); w=w-dw
    if np.max(np.abs(dw))<1e-15*np.max(np.abs(w)): break
s=2j*w                     # left half-plane roots (Re s<0)
den=1j*2*w*(1-sig*np.cos(w))   # s - sinh s
K=int(TMAX/(2*np.pi)/4)        # keep |Im s| well inside the t-grid
terms=np.empty(K,complex)
for k in range(K):
    P=np.exp(logP(-s[k]))
    terms[k]=P*P/den[k]
tailsum=np.sum(1/den[K:])
# roots beyond J: 1/den ~ -1/(2|w|^2), |w|~(j+1/2)pi  => 2Re(sum_{j>J}) ~ -1/(pi^2 (J+1/2))
tailJ=-1/(np.pi**2*(J+0.5))
S=2*np.real(np.sum(terms)+tailsum)+tailJ
vtv=d0/6-S/24
print('K=%d  sum=%.14f  <V,TV>=%.13f  (grid 0.039958599729)'%(K,S,vtv))
C=12*np.sqrt(3)/np.sqrt(np.pi)
print('c1 = C<V,TV> = %.12f (paper 0.468572932794); c1 from grid = %.12f'%(C*vtv, C*0.039958599729))
# convergence in K
for KK in [K//8,K//4,K//2]:
    S2=2*np.real(np.sum(terms[:KK])+np.sum(1/den[KK:]))+tailJ
    print('  K=%d <V,TV>=%.13f'%(KK,d0/6-S2/24))
print('time %.1f s'%(time.time()-t0))
