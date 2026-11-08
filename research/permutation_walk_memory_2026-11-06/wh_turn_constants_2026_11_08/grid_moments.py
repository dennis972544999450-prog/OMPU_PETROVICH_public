# moments of ladder height H from <V,(1-t)^{m+2}> = (m+2) E[H] E[H^{m+1}], Richardson in h
import numpy as np, importlib.util, sys
spec=importlib.util.spec_from_file_location('gc','grid_check.py')
src=open('grid_check.py').read().split('res={}')[0]
ns={}; exec(src,ns)
solve=ns['solve']
EH=1/np.sqrt(12)
res={}
for h in [0.02,0.01,0.005,0.0025]:
    x,V,w=solve(h,12.0)
    m=x<1; xm=x[m]; Vm=V[m]
    mom=[]
    for k in range(1,7):   # E[H^k]
        val=(Vm@(1-xm)**(k+1))*h/((k+1)*EH)
        mom.append(val)
    res[h]=np.array(mom)
hs=sorted(res,reverse=True)
R1=[(4*res[hs[i+1]]-res[hs[i]])/3 for i in range(3)]
R2=[(16*R1[i+1]-R1[i])/15 for i in range(2)]
for k in range(6):
    print('E[H^%d] = %.12f  (%.12f)'%(k+1,R2[1][k],R2[0][k]))
