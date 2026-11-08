# P_m(inf) for m turns after a long run: <P(H>.), T^{m-1} q> / <P(H>.), T^{m-1} 1>, q=(1-u)^2/2
# polynomials exact in Fractions; moments E[H^n] from b-coefficients (b_odd = -(odd root sums), b_even rational)
from fractions import Fraction as Fr
import numpy as np
from math import factorial
def T(p):  # p: dict power->coef in t ; returns dict in x: sum c_k (1-x)^{k+2}/((k+1)(k+2))
    out={}
    for k,c in p.items():
        cc=c/((k+1)*(k+2)); n=k+2
        for i in range(n+1):
            from math import comb
            out[i]=out.get(i,0)+cc*comb(n,i)*(-1)**i
    return out
q={0:Fr(1,2),1:Fr(-1),2:Fr(1,2)}; one={0:Fr(1)}
# b coefficients: b_even from log(12Q/(-s^2)) series; b_odd from root sums
# 12Q/(-s^2) = sum_i 24 s^{2i}/(2i+4)!  (for s real: sinh series, all +)
N=12
ser=[Fr(0)]*(2*N+1)
for i in range(N+1):
    if 2*i<=2*N: ser[2*i]=Fr(24,factorial(2*i+4))
# log of series
def logser(a,n):
    # a[0]=1
    l=[Fr(0)]*(n+1)
    for k in range(1,n+1):
        l[k]=a[k]-sum(Fr(j,k)*l[j]*a[k-j] for j in range(1,k))
    return l
lg=logser(ser,2*N)
b={k:lg[k]/2 for k in range(2,2*N+1,2)}
# odd: b_j = -p_j/j (j>=3), b_1 = -1/2 - p_1 ; p_j = 2^{1-j} i^{1-j} sum Im(w^-j)
J=1000000
j=np.arange(1,J+1); sig=np.where(j%2==0,1.0,-1.0)
a=(j+0.5)*np.pi; w=a+1j*np.arccosh(a)
for it in range(60):
    dw=(np.sin(w)-sig*w)/(np.cos(w)-sig); w=w-dw
    if np.max(np.abs(dw))<1e-15*np.max(np.abs(w)): break
aJ=(J+1)*np.pi
S1=np.sum(np.imag(1/w))-(np.log(2*aJ)+1)/(np.pi*aJ)
bf={1:-0.5-S1}
for jj in [3,5,7]:
    Sj=np.sum(np.imag(w**(-float(jj))))
    pj=(2.0**(1-jj))*((1j)**(1-jj)).real*Sj
    bf[jj]=-pj/jj
for k,v in b.items(): bf[k]=float(v)
print('b:',{k:('%.15g'%bf[k]) for k in sorted(bf) if k<=8})
# a_n = coeffs of exp(sum b_j s^j)
M=8
bb=[0.0]+[bf.get(k,0.0) for k in range(1,M+1)]
aa=[1.0]+[0.0]*M
for n in range(1,M+1):
    aa[n]=sum(k*bb[k]*aa[n-k] for k in range(1,n+1))/n
EH=1/np.sqrt(12)
mom={n:EH*(-1)**(n-1)*factorial(n)*aa[n-1] for n in range(1,M+1)}
print('E[H^n]:',{n:'%.12f'%mom[n] for n in mom})
def pair(p):  # <P(H>.), p> = sum c_k E[H^{k+1}]/(k+1)
    return sum(float(c)*mom[k+1]/(k+1) for k,c in p.items())
num,den=q,one
for m in range(1,4):
    print('P_%d(inf) = %.12f'%(m, pair(num)/pair(den)))
    num,den=T(num),T(den)
print('paper: P_1 0.3151600752  P_2 0.2793320208  P_3 0.28519033')
