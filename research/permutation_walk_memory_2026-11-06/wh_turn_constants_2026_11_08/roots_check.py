# Roots w of sin w = sigma*w in the open first quadrant (sigma=(-1)^j near (j+1/2)pi)
# Test: delta0 = 1/2 + sum_w Im(1/w);  gamma3 = -(1/12) sum_w Im(w^-3)
import numpy as np
def roots(J):
    j=np.arange(1,J+1); sig=np.where(j%2==0,1.0,-1.0)
    a=(j+0.5)*np.pi; w=a+1j*np.arccosh(a)
    for it in range(60):
        f=np.sin(w)-sig*w; fp=np.cos(w)-sig
        dw=f/fp; w=w-dw
        if np.max(np.abs(dw))<1e-15*np.max(np.abs(w)): break
    res=np.max(np.abs(np.sin(w)-sig*w)/np.abs(w))
    return w,res
for J in [1000,10000,100000,1000000]:
    w,res=roots(J)
    S1=np.sum(np.imag(1/w)); S3=np.sum(np.imag(w**-3.0))
    # tail of Im(1/w) ~ -beta/|w|^2, beta~log(2a): integrate asymptotically from J+1/2
    # use simple tail estimate: sum_{j>J} -log(2(j+1/2)pi)/((j+1/2)pi)^2 ~ -(log(2 a_J)+1)/(pi a_J), a_J=(J+1)pi
    aJ=(J+1)*np.pi
    tail1=-(np.log(2*aJ)+1)/(np.pi*aJ)
    print(J, 'max rel resid %.1e'%res, 'first roots', w[:2] if J==1000 else '',
          ' delta0 = %.12f (+tail %.12f)'%(0.5+S1, 0.5+S1+tail1), ' gamma3 = %.15f'%(-S3/12))
print('targets: delta0 0.227350780092  gamma3 0.000991025277641')
