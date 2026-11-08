# Brute force for paper §6.1: M_m(psi) = <L^{m-1} psi, 1>,  M_m(1)/M_m(1-x) = <U,1> + <V1,1>/m + O(m^-2)
# (M_m(1-x) = u_m exactly by Sparre Andersen; the ratio cancels part of the grid error.)
import numpy as np, scipy.sparse as sp, time, sys
def run(h, mmax, X):
    x=(np.arange(int(round(X/h)))+0.5)*h; N=len(x); B=int(round(1/h))
    diags=[]; offs=[]
    for d in range(-B,B+1):
        val=max(1-abs(d)*h,0)*h
        if val>0: diags.append(np.full(N-abs(d),val)); offs.append(d)
    K=sp.diags(diags,offs,format='csr')
    m1=x<1
    f1=np.where(m1,1.0,0.0); f2=np.where(m1,1-x,0.0)
    out={}
    for m in range(1,mmax+1):
        if m>1: f1=K@f1; f2=K@f2
        if m in CHECK: out[m]=(f1.sum()*h)/(f2.sum()*h)
    return out
CHECK=[125,250,500,1000]
t0=time.time()
res={}
for h in [0.02,0.01,0.005]:
    res[h]=run(h,1000,1+8*np.sqrt(1000/6)+5)
    print(h, {m:'%.12f'%v for m,v in res[h].items()}, '%.0fs'%(time.time()-t0)); sys.stdout.flush()
hs=[0.02,0.01,0.005]
ext={}
for m in CHECK:
    a=[res[h][m] for h in hs]
    r1=[(4*a[1]-a[0])/3,(4*a[2]-a[1])/3]; ext[m]=(16*r1[1]-r1[0])/15
    print('m=%d h-extrap %.12f (R1 %.12f)'%(m,ext[m],r1[1]))
U1=1.0/0.5*0  # placeholder
# fit ext[m] = A + B/m + C/m^2 + D/m^3 on the four m
ms=np.array(CHECK,float); M=np.vstack([ms**0,1/ms,1/ms**2,1/ms**3]).T
coef=np.linalg.solve(M,np.array([ext[m] for m in CHECK]))
print('fit: <U,1>=%.12f  <V1,1>=%.12f  (paper -0.760599464113; formula -0.760599353809)'%(coef[0],coef[1]))
