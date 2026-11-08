import numpy as np
src=open('grid_check.py').read().split('res={}')[0]; ns={}; exec(src,ns); solve=ns['solve']
res={}
for h in [0.02,0.01,0.005,0.0025]:
    x,V,w=solve(h,12.0); m=x<1; xm=x[m]
    Kt=np.clip(1-xm[:,None]-xm[None,:],0,None)*h
    f=V[m]; q=(1-xm)**2/2; out=[]
    for k in range(4):
        f=Kt@f; out.append((f@q)/f.sum())
    EH7=(V[m]@(1-xm)**8)*h/(8/np.sqrt(12))
    res[h]=np.array(out+[EH7])
hs=sorted(res,reverse=True)
R1=[(4*res[hs[i+1]]-res[hs[i]])/3 for i in range(3)]
R2=[(16*R1[i+1]-R1[i])/15 for i in range(2)]
print('P_1..P_4, E[H^7]:', ['%.12f'%v for v in R2[1]], ' prev', ['%.12f'%v for v in R2[0]])
