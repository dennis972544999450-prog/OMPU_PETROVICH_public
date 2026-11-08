import numpy as np
src=open('vtv_residue.py').read().split('# sanity')[0]; ns={}; exec(src,ns); logP=ns['logP']
src2=open('grid_check.py').read().split('res={}')[0]; ns2={}; exec(src2,ns2); solve=ns2['solve']
h=0.0025; x,V,w=solve(h,12.0); m=x<1; xm=x[m]
Kt=np.clip(1-xm[:,None]-xm[None,:],0,None)*h
TV=Kt@V[m]; tail=TV*np.sqrt(12)        # P(H>u) on midpoints
for s in [0.5,1,2,5,1+3j,4.5-8.4j]:
    Pg=s*np.sum(np.exp(-s*xm)*tail)*h   # 1 - E e^{-sH} = s int e^{-su} P(H>u) du
    Ps=np.exp(logP(complex(s)))
    print(s,'schwarz',np.round(Ps,10),'grid',np.round(Pg,10))
