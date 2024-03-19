import numpy as np
import findpeak as fp


def find_pairs(ivall,names):
    x0=[]
    x1=[]
    for i in names[ivall]:
        ed=i.split('->')
        x=[i for i in names[ivall] if ed[0] in i]
        if len(x)>1:
            x0.append(x)
        x=[i for i in names[ivall] if ed[1] in i]
        if len(x)>1:
            x1.append(x)
    return x0,x1

#w=np.arange(150,9261,300)
#out = [np.load(f'scores_{i}.npy') for i in range(150,9260,300)]

def md_window_heatmap(out,w,band):
    md=np.zeros(9261)
    x=np.arange(w/2,9261-(w/2),1).astype(int)
    m=out
    md[x]=out[:,band]
    return md

# MD=np.array([md_window_heatmap(out[i],w[i],1060) for i in range(0,31)])
#ivall25=[np.where(i.max(0)>0.25)[0] for i in tst]



def createindexarray(w,t,index):
    rowdimen=t-w+1
    a=np.arange(0,rowdimen*(t+1),(t+1))
    return np.arange(a[index],a[index]+w)


def createT(w,t):
    rowdimen=t-w+1
    index=np.concatenate(([createindexarray(w,t,a) for a in range(rowdimen)]))
    d=np.zeros(rowdimen*t)
    d[index]=1
    return np.array([d[i:i+t] for i in np.arange(0,len(d),t)]).astype(int)

def createdivider(T):
    return np.sum(T,axis=0)


def computeavg(w,t,track):
    T=createT(w,t)
    div=createdivider(T)
    return np.dot(track,T)/div
   
def gettime(time):
    return np.arange(time)

def getT(w,timearr):
    return((timearr[:len(timearr)-w][:,None]<=timearr) & (timearr[:len(timearr)-w][:,None]+w>timearr)).astype(int)
    

def loopoverwindow(time,windows):
    tarr=gettime(time)
    return [getT(w,tarr) for w in windows]

class Scandot():
    def __init__(self,tracks,windows,time):
        self.time=time
        self.windows=windows
        self.T=loopoverwindow(time,windows)
        if tracks[0].shape[1] != self.T[0].shape[0]:
            self.tracks=[i.T for i in tracks]
        self.tracks=tracks
        print(self.tracks[0].shape,self.T[0].shape)
    def allwinalledge(self,window):
        return np.dot(self.tracks[window],self.T[window])/self.T[window].sum(0)

    def converttoheatmap(self,dotout):
        #return np.array([[dotout[i][j] for j in range(0,1107)] for i in np.arange(len(self.windows))])
        return np.array([[dotout[i][j] for i in np.arange(len(self.windows))] for j in range(dotout[0].shape[0])])
        
def performdotaverage(edge,tracks,T):
    return np.dot(tracks[edge].T,T[edge])/T[edge].sum(0)


def findwindowwithmax(allwindow):
    return np.array([argmax(amax(i,axis=1)) for i in allwindow])

#heatmap=np.array([[heatmap[i][j] for i in range(0,31)] for j in range(0,1107)])
def getmaxfromheat(heatmap):
    return np.array([np.argmax(np.amax(i,axis=1)) for i in heatmap])

# This next line produces all the track information for a given set of
#allt=np.array([fp.Track(heatmap[e][maxargs[e]],e,maxargs[e],bands=True,th_bw=10,th_h=0.1) for e in range(len(maxargs))])

def findbandlocs(allt,maxargs,windows=None):
    #if winodws not given then useall windows
    if windows is None:
        #first determine the number of bands in each track
        nums=np.array([i.numbands for i in allt])
        #store the edges with 1 or more bands
        iv=np.where(nums>0)[0]
        #return a list of all band locations
        return iv,[i.band_Max_loc for i in allt[iv]]
    #if window range given, provide events only using range of windows
    a=np.where((maxargs>=windows[0])&(maxargs<windows[1]))[0]
    w=np.where(np.array([i.numbands for i in allt[a]])>0)[0]
    return a[w],[i.band_Max_loc for i in allt[a[w]]]


def findbandlocs_a(allt,a):
    #first determine the number of bands in each track
    nums=np.array([i.numbands for i in allt])
    #store the edges with 1 or more bands
    iv=np.where(nums>0)[0]
    #return a list of all band locations
    return iv,[i.band_Max_loc for i in allt[iv]]


def geteventinfo(allt):
    allbands=np.concatenate([j.bands for j in allt])
    return np.array([[a.variable,a.max_loc,a.width,a.area] for a in allbands])

def getiv(events):
    return np.array(list(set(events[:,0])))

def producenetwork(nodelist,iv):
    network=[]
    for i in range(len(iv)):
        index=iv[i]
        network.append([(index,nodelist[i][j]) for j in range(len(nodelist[i]))])
    return np.concatenate(network).astype(int)

def sortnetwork(network):
    return network[np.argsort(network[:,1])]

def getedges(sortedN):
    return np.concatenate([[(sortedN[k][0],sortedN[j][0]) for j in range(k,len(sortedN)) if sortedN[j][0] != sortedN[k][0]] for k in range(len(sortedN))][:-1]).astype(int)


def splitedge(edgename):
    return np.concatenate((edgename.split('->')[0].split('_'),edgename.split('->')[1].split('_'))) 

def computeedgedistance(edge,distmatrix,names):
    cs1=edge[0].split('->')
    cs2=edge[1].split('->')
    c1=np.where(names==cs1[0])[0]
    c2=np.where(names==cs1[1])[0]
    c3=np.where(names==cs2[0])[0]
    c4=np.where(names==cs2[1])[0]
    d=[]
    #distance c1-c3
    d.append(np.amax([distmatrix[c1,c3],distmatrix[c3,c1]]))
    #distance c1-4
    d.append(np.amax([distmatrix[c1,c4],distmatrix[c4,c1]]))
    #distance c2-c3
    d.append(np.amax([distmatrix[c2,c3],distmatrix[c3,c2]]))
    #distance c2-c4
    d.append(np.amax([distmatrix[c2,c4],distmatrix[c4,c2]]))
    return np.amin(d) 

def computeedgetimediff(edge,N):
    return np.abs(N[np.where(N==edge[0])[0]][0][1]-N[np.where(N==edge[1])[0]][0][1])

def distmatrix(edgenames,distmatrix,resnames,iv):
    return np.array([[computeedgedistance([edgenames[i],edgenames[j]],distmatrix,resnames) for i in iv] for j in iv])

def getallt(peakth,windows=None,heatmap=None):
    if heatmap is None:
        heatmap=np.load('heatmap.npy')
    maxargs=getmaxfromheat(heatmap)
    allt=np.array([fp.Track(heatmap[e][maxargs[e]],e,maxargs[e],bands=True,th_bw=10,th_h=peakth) for e in range(len(maxargs))])
    iv,nodelist=findbandlocs(allt,maxargs,windows)
    return allt,iv,maxargs

def getalltivandevents(peakth,windows=None,heatmap=None,eventsonly=False):
    if heatmap is None:
        heatmap=np.load('heatmap.npy')
    maxargs=getmaxfromheat(heatmap)
    allt=np.array([fp.Track(heatmap[e][maxargs[e]],e,maxargs[e],bands=True,th_bw=10,th_h=peakth) for e in range(len(maxargs))])
    iv,nodelist=findbandlocs(allt,maxargs,windows)
    if eventsonly:
        return sortnetwork(producenetwork(nodelist,iv))
    return allt,iv,sortnetwork(producenetwork(nodelist,iv)),maxargs
