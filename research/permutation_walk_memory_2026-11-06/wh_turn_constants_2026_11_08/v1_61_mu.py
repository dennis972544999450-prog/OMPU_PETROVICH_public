# mu_1(psi) = <V1,psi>/<U,psi> with V1 = U/2 + W0 + cU, c = -1/2 - <W0,1-x>; psi = T f1, T^2 f1, f1 = 1-x
import numpy as np
src=open('v1_61_check2.py').read().split('res={h:run')[0]; ns={}; exec(src,ns)
solve=ns['solve']; s3=np.sqrt(3)
def run(h,X=12.0):
    x,V,w=solve(h,X); N=len(x); d0=w[len(w)//2]
    D=np.abs(x[:,None]-x[None,:]); K=np.clip(1-D,0,None)*h
    Dr=np.abs(x[:,None]-(2*X-x[None,:])); K+=np.clip(1-Dr,0,None)*h
    P=-2*s3*x**3-6*s3*d0*x**2
    c3=-2*s3; c2=-6*s3*d0
    A=1-x; a=x-1
    F=lambda y: A*(c3*y**4/4+c2*y**3/3)+(c3*y**5/5+c2*y**4/4)
    b=np.where(x<1,F(0.0)-F(a),0.0)
    R=np.linalg.solve(np.eye(N)-K,s3*(w-d0)-b)
    W0=P+R; m=x<1; xm=x[m]; U=np.sqrt(12)*V[m]; W=W0[m]
    c=-0.5-(W@(1-xm))*h
    V1=U/2+W+c*U
    Kt=np.clip(1-xm[:,None]-xm[None,:],0,None)*h
    f1=1-xm; p1=Kt@f1; p2=Kt@p1
    mu=lambda p:(V1@p)/(U@p)
    return np.array([V1.sum()*h, mu(p1), mu(p2), 0.5+mu(p2)-mu(p1)])
res={h:run(h) for h in [0.02,0.01,0.005,0.0025]}
hs=sorted(res,reverse=True)
R1=[(4*res[hs[i+1]]-res[hs[i]])/3 for i in range(3)]
R2=[(16*R1[i+1]-R1[i])/15 for i in range(2)]
for nm,i,pap in [('<V1,1>',0,-0.760599464113),('mu1(T f1)',1,0.1244750302),('mu1(T^2 f1)',2,0.1117838366),('C(-+,+-)',3,0.4873088064)]:
    print('%-12s %.12f %.12f   paper %.10f'%(nm,R2[0][i],R2[1][i],pap))
