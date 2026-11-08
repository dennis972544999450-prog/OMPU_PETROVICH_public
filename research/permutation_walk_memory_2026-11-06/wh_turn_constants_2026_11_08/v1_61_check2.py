# Claim: paper §6.1 correction functional V1_61 = U/2 + W, (I-L)W = U/2 on [0,inf), fixed by <V1_61,1-x>=0.
# => <V1_61,1> = <W0,1> - <W0,1-x><U,1> for ANY polynomial-growth particular solution W0.
# W0 = P + R, P = -2 sqrt3 x^3 - 6 sqrt3 d0 x^2 (exact on the full line), R bounded: (I-K)R = g.
import numpy as np
src=open('grid_check.py').read().split('res={}')[0]; ns={}; exec(src,ns); solve=ns['solve']
d0=0.227350780091995; s3=np.sqrt(3)
def run(h,X=12.0):
    global d0
    x,V,w=solve(h,X); N=len(x); d0=w[len(w)//2]
    D=np.abs(x[:,None]-x[None,:]); K=np.clip(1-D,0,None)*h
    Dr=np.abs(x[:,None]-(2*X-x[None,:])); K+=np.clip(1-Dr,0,None)*h
    P=-2*s3*x**3-6*s3*d0*x**2
    # boundary term b(x)=int_{x-1}^0 (1-x+y) P(y) dy for x<1, exact polynomial integral
    def Pint(x0):
        # int_{x0-1}^0 (1-x0+y)(-2s3 y^3 - 6 s3 d0 y^2) dy
        a=x0-1.0
        def F(y): # antiderivative of (1-x0+y)*(c3 y^3 + c2 y^2)
            c3=-2*s3; c2=-6*s3*d0; A=1-x0
            return A*(c3*y**4/4+c2*y**3/3)+(c3*y**5/5+c2*y**4/4)
        return F(0.0)-F(a)
    b=np.where(x<1,Pint(x),0.0)
    g=s3*(w-d0)-b
    R=np.linalg.solve(np.eye(N)-K,g)
    W0=P+R; m=x<1; xm=x[m]
    U=np.sqrt(12)*V
    I1=W0[m].sum()*h; I1x=(W0[m]@(1-xm))*h; U1=U[m].sum()*h; U1x=(U[m]@(1-xm))*h
    return np.array([I1-I1x*U1, U1x, R[-1]-R[len(R)//2]])
res={h:run(h) for h in [0.02,0.01,0.005,0.0025]}
for h in res: print(h, res[h])
hs=sorted(res,reverse=True)
R1=[(4*res[hs[i+1]]-res[hs[i]])/3 for i in range(3)]
R2=[(16*R1[i+1]-R1[i])/15 for i in range(2)]
print('R1', ['%.12f'%r[0] for r in R1]); print('R2', ['%.12f'%r[0] for r in R2], ' paper -0.760599464113')
