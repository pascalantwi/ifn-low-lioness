import numpy as np
rng=np.random.default_rng(1)
def cov(X): mu=X.mean(0); D=X-mu; return D.T@D/X.shape[0]
def shr(S,l): return (1-l)*S+l*np.diag(np.diag(S))
def pcor_from(S): O=np.linalg.inv(S); d=np.sqrt(np.diag(O)); P=-O/np.outer(d,d); np.fill_diagonal(P,1); return P,O
def pear(S): d=np.sqrt(np.diag(S)); return S/np.outer(d,d)
G,N=8,2000
A=np.eye(G)+np.diag(np.full(G-1,.35),1)+np.diag(np.full(G-1,.35),-1); Sig=np.linalg.inv(A)
X=rng.multivariate_normal(np.zeros(G),Sig,size=N)
iu=np.triu_indices(G,1)
for lam in [0.0,0.3]:
    S=cov(X); P,O=pcor_from(shr(S,lam)); mu=X.mean(0)
    errs=[];scale=[]
    for q in range(40):
        Xm=np.delete(X,q,0); Pm,_=pcor_from(shr(cov(Xm),lam))
        e=N*P-(N-1)*Pm
        d=X[q]-mu; u=O@d; Dd=np.diag(d**2)
        M=(1-lam)*np.outer(u,u)+lam*O@Dd@O
        sq=np.sqrt(np.diag(O)); Mt=M/np.outer(sq,sq)
        approx=P+Mt+P*(np.diag(Mt)[:,None]+np.diag(Mt)[None,:])/2
        errs.append(np.abs(e-approx)[iu].max()); scale.append(np.abs(e-P)[iu].max())
    print(f"partial lam={lam}: max|exact-approx|={max(errs):.3g}  typical |e-rho|={np.median(scale):.3g}")
# Pearson
S=cov(X); R=pear(S); mu=X.mean(0); sd=np.sqrt(np.diag(S)); errs=[]
for q in range(40):
    Rm=pear(cov(np.delete(X,q,0))); e=N*R-(N-1)*Rm; z=(X[q]-mu)/sd
    approx=np.outer(z,z)+R*(1-(z[:,None]**2+z[None,:]**2)/2)
    errs.append(np.abs(e-approx)[iu].max())
print(f"pearson: max|exact-approx|={max(errs):.3g}")
# expectation checks with first-order formula (lam=0): spread invariance; balanced mean shift
P,O=pcor_from(cov(X)); sq=np.sqrt(np.diag(O))
def edges(D):
    U=(D@O)/sq; return U[:,0]*U[:,1]+P[0,1]*(1+(U[:,0]**2+U[:,1]**2)/2)
Z=rng.multivariate_normal(np.zeros(G),Sig,size=200000)
print("rho01=%.4f  E[e] k=1: %.4f  k=2: %.4f"%(P[0,1],edges(Z).mean(),edges(2*Z).mean()))
delta=np.full(G,0.8)
print("balanced shift: E[e|+d/2]=%.4f  E[e|-d/2]=%.4f"%(edges(Z+delta/2).mean(),edges(Z-delta/2).mean()))
print("unbalanced (ref mean at group B): E[e|A]=%.4f E[e|B]=%.4f"%(edges(Z+delta).mean(),edges(Z).mean()))
