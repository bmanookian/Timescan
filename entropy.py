import numpy as np


def encode(c):
    try:
        b=np.ones(c.shape[1],dtype=int)
    except Exception:
        c=np.column_stack(c)
        b=np.ones(c.shape[1],dtype=int)
    b[:-1]=np.cumprod((c[:,1:].max(0)+1)[::-1])[::-1]
    return np.sum(b*c,1)

def mi_p(A):
    X,Y=A
    return H(X)+H(Y)-joinH((X,Y))

def H(i):
        """entropy of labels"""
        p=np.unique(i,return_counts=True)[1]/i.size
        return -np.sum(p*np.log2(p))

def joinH(i):
	pair=np.column_stack((i))
	en=encode(pair)
	p=np.unique(en,return_counts=True)[1]/len(en)
	return -np.sum(p*np.log2(p))


