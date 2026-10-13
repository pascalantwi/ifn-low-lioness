import numpy as np
rng=np.random.default_rng(7)
def cov(X): mu=X.mean(0); D=X-mu; return D.T@D/X.shape[0]
def pear(S): d=np.sqrt(np.diag(S)); return S/np.outer(d,d)
def pcor(S,l=0.3):
    S=(1-l)*S+l*np.diag(np.diag(S)); O=np.linalg.inv(S); d=np.sqrt(np.diag(O)); P=-O/np.outer(d,d); np.fill_diagonal(P,1); return P
G,n=20,100
A=np.eye(G)+np.diag(np.full(G-1,.4),1)+np.diag(np.full(G-1,.4),-1); Sig=np.linalg.inv(A)
R=rng.multivariate_normal(np.zeros(G),Sig,size=n); T=rng.multivariate_normal(np.zeros(G),Sig,size=30)
iu=np.triu_indices(G,1)
for name,f in [("Pearson (SSN vs LIONESS)",pear),("partial (P-SSN vs LIONESS-partial)",pcor)]:
    P=f(cov(R)); ssn=[];lio=[]
    for t in T:
        Pp=f(cov(np.vstack([R,t])))
        ssn.append((Pp-P)[iu])                 # SSN delta-correlation (Liu 2016)
        lio.append(((n+1)*Pp-n*P)[iu])         # LIONESS add-one-in, same reference
    ssn=np.array(ssn); lio=np.array(lio)
    err=np.abs(ssn-(lio-P[iu])/(n+1)).max()
    print(f"{name}: max |SSN - (LIONESS - rho)/(n+1)| = {err:.2e}")
