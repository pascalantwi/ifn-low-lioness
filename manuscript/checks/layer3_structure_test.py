import numpy as np
rng=np.random.default_rng(11)
def pcor(X,l=0.2):
    X=X-X.mean(0); S=X.T@X/len(X); S=(1-l)*S+l*np.diag(np.diag(S))
    O=np.linalg.inv(S); d=np.sqrt(np.diag(O)); return -O/np.outer(d,d)
def stat(A,B,std):
    if std: A=(A-A.mean(0))/A.std(0); B=(B-B.mean(0))/B.std(0)
    return np.linalg.norm(pcor(A)-pcor(B))
def ptest(A,B,std,nperm=199):
    X=np.vstack([A,B]); n=len(A); obs=stat(A,B,std); c=0
    for _ in range(nperm):
        i=rng.permutation(len(X)); c+=stat(X[i[:n]],X[i[n:]],std)>=obs
    return (c+1)/(nperm+1)
G,n=10,80
A0=np.eye(G)+np.diag(np.full(G-1,.4),1)+np.diag(np.full(G-1,.4),-1); Sig=np.linalg.inv(A0)
def gen(scen):
    hc=rng.multivariate_normal(np.zeros(G),Sig,n)
    if scen=="S0": ca=rng.multivariate_normal(np.zeros(G),Sig,n)
    if scen=="S2a":  # spread only: per-gene scales differ, correlations unchanged
        D=np.diag(rng.uniform(1.2,2.0,G)); ca=rng.multivariate_normal(np.zeros(G),D@Sig@D,n)
    if scen=="S2b":  # hidden subtypes shifted in opposite directions, no net mean shift
        ca=rng.multivariate_normal(np.zeros(G),Sig,n); s=np.where(rng.random(n)<.5,1,-1)
        shift=np.zeros(G); shift[:4]=1.0; ca=ca+np.outer(s,shift)
    return hc,ca
for scen in ["S0","S2a","S2b"]:
    for std in [False,True]:
        rej=np.mean([ptest(*gen(scen),std)<0.05 for _ in range(100)])
        print(f"{scen:4s} per-group standardised={std!s:5s}: rejection rate of layer 3 = {rej:.2f}")
