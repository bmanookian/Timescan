import numpy as np

# Load numpys

def loadnumpys(heatmap=False):
	eds=np.load('edgenames.npy')
	nod=np.load('nodenames.npy')
	tks=np.load('tracks.npy')
	iv=np.load('tracks_cutoff.npy')
	evs=np.load('events.npy')
	return eds,nod,tks,iv,evs


def getT(thresh,heatmap=heatmap,windows=None):
    if windows is not None:
        maxargs=np.array([np.argmax(np.amax(i,axis=1)) for i in heatmap[:,:windows,:]])
    else:
        maxargs=np.array([np.argmax(np.amax(i,axis=1)) for i in heatmap])
    T=np.array([heatmap[i][maxargs[i]] for i in range(heatmap.shape[0])])
    iv=np.unique(np.where(T>thresh)[0])
    return T,iv

def eventsinrange(events,lower,upper):
    return np.array([e[0] for e in events if (e[1]>=lower) & (e[1]<=upper)])

def peaksinrange(intv,T,thresh=0.2,inclusive='all'):
    Tb=T>thresh
    if inclusive=='all':
        Edb=np.array([np.any(Tb[i,intv[0]:intv[1]]) for i in range(Tb.shape[0])])
        return Edb
    if inclusive=='before':
        Edb=np.array([(np.any(Tb[i,intv[0]:intv[1]]))&(np.all(~Tb[i,intv[1]:])) for i in range(Tb.shape[0])])
        return Edb
    if inclusive=='after':
        Edb=np.array([(np.any(Tb[i,intv[0]:intv[1]]))&(np.all(~Tb[i,:intv[0]])) for i in range(Tb.shape[0])])
        return Edb
    if inclusive=='only':
        Edb=np.array([(np.any(Tb[i,intv[0]:intv[1]]))&(np.all(~Tb[i,:intv[0]]))&(np.all(~Tb[i,intv[1]:])) for i in range(Tb.shape[0])])
        return Edb


# Below is code for getting nestedMI or weighted degree for all nodes

def getV(T):
    V=np.vstack((T[0],T[0]))
    for i in range(1,T.shape[0]):
        V=np.vstack((V,T[i],T[i]))
    return V


def splitedges_unq(edges,unique=True):
    splitedges=np.concatenate([edges[i].split('->') for i in range(edges.shape[0])])
    if unique==False:
        return splitedges
    return splitedges,np.unique(splitedges)


def getindx_map(splitedges,unq_split):
    return [np.where(splitedges==x)[0] for x in unq_split]

def getnestd(V,indx_map,thresh):
    return np.array([np.sum(V[x]>thresh,axis=0) for x in indx_map])

def getnestMI(edges,T):
    V=getV(T)
    splitedges,unq_split=splitedges_unq(edges)
    indx_map=getindx_map(splitedges,unq_split)
    return np.array([np.sum(V[x],axis=0) for x in indx_map])

