import numpy as np

# Load numpys

def loadnumpys(heatmap=False):
	eds=np.load('edgenames.npy')
	nod=np.load('nodenames.npy')
	tks=np.load('tracks.npy')
	iv=np.load('tracks_cutoff.npy')
	evs=np.load('events.npy')
	return eds,nod,tks,iv,evs

# find list of edges with peaks in range (lower-upper)

def eventsinrange(events,lower,upper):
    return np.array([e[0] for e in events if (e[1]>=lower) & (e[1]<=upper)])
