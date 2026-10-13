import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
rng=np.random.default_rng(21)
G,n=10,80
A0=np.eye(G)+np.diag(np.full(G-1,.4),1)+np.diag(np.full(G-1,.4),-1); Sig=np.linalg.inv(A0)
def rewired():
    A=A0.copy(); A[0,1]=A[1,0]=-0.4; A[2,3]=A[3,2]=0.0; A[0,3]=A[3,0]=0.35
    while np.min(np.linalg.eigvalsh(A))<=0.05: A=A+0.05*np.eye(G)
    return np.linalg.inv(A)
SigR=rewired()
def flag(X,k=3,thr=10):
    Z=PCA(k).fit_transform(X-X.mean(0))
    b=[GaussianMixture(m,covariance_type='full',n_init=3,random_state=0).fit(Z).bic(Z) for m in (1,2)]
    return (b[0]-b[1])>thr
res={}
for scen in ["S0","S2b","S3"]:
    fl=[]
    for _ in range(200):
        if scen=="S0": X=rng.multivariate_normal(np.zeros(G),Sig,n)
        if scen=="S2b":
            X=rng.multivariate_normal(np.zeros(G),Sig,n); s=np.where(rng.random(n)<.5,1,-1); sh=np.zeros(G); sh[:4]=1.0; X=X+np.outer(s,sh)
        if scen=="S3": X=rng.multivariate_normal(np.zeros(G),SigR,n)
        fl.append(flag(X))
    print(f"{scen}: proportion of patient groups flagged as 'subgroups' = {np.mean(fl):.2f}")
