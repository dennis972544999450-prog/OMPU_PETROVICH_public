# Independent grid check: V on [0,X] (midpoint Nystrom, reflecting far end), then
# P_max = <TV,(1-u)^2/2>/<TV,1>, P_min = <T^2V,(1-u)^2/2>/<T^2V,1>, identity TV = E[H] P(H>u) moments,
# <V,TV>, delta0 = w(inf). Richardson in h.
import numpy as np, sys
def solve(h, X):
    x=(np.arange(int(round(X/h)))+0.5)*h; N=len(x)
    D=np.abs(x[:,None]-x[None,:]); K=np.clip(1-D,0,None)*h
    Dr=np.abs(x[:,None]-(2*X-x[None,:])); K+=np.clip(1-Dr,0,None)*h
    g=np.where(x<1,(1-x)**3/6,0.0)
    w=np.linalg.solve(np.eye(N)-K,g)
    return x, x+w, w
def T_on_grid(x,f,h):
    # (Tf)(u)=int_0^{1-u}(1-u-t) f(t) dt on midpoints of [0,1]; midpoint rule with kernel (1-u-t)_+
    m=x<1; xm=x[m]; fm=f[m]
    Kt=np.clip(1-xm[:,None]-xm[None,:],0,None)*h
    return xm, Kt@fm
res={}
for h in [0.02,0.01,0.005,0.0025]:
    x,V,w=solve(h,12.0)
    xm,TV=T_on_grid(x,V,h)
    _,T2V=T_on_grid(np.concatenate([xm,x[len(xm):]]),np.concatenate([TV,np.zeros(len(x)-len(xm))]),h)
    q=(1-xm)**2/2
    pmax=(TV@q)/TV.sum(); pmin=(T2V@q)/T2V.sum()
    vtv=(V[:len(xm)]@TV)*h
    mom0=TV.sum()*h          # should be E[H]^2 = 1/12
    mom1=(xm@TV)*h           # E[H] E[H^2]/2 = delta0/12
    res[h]=np.array([pmax,pmin,vtv,mom0,mom1,w[len(w)//2]])
    print(h, ' '.join('%.12f'%v for v in res[h])); sys.stdout.flush()
hs=sorted(res,reverse=True)
R1=[(4*res[hs[i+1]]-res[hs[i]])/3 for i in range(len(hs)-1)]
R2=[(16*R1[i+1]-R1[i])/15 for i in range(len(R1)-1)]
names=['P_max','P_min','<V,TV>','int TV (1/12=0.083333333333)','int u TV (d0/12)','delta0']
for i,nm in enumerate(names):
    print('%-32s R1 %.12f %.12f %.12f | R2 %.12f %.12f'%(nm,R1[0][i],R1[1][i],R1[2][i],R2[0][i],R2[1][i]))
