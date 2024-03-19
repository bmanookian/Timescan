import numpy as np


class Track():
    def __init__(self,X,var,windowind=None,bands=False,th_bw=None,th_h=None,compute_stat=False):
        self.X=X
        self.var=var
        self.bands = bands
        self.windowind=windowind
        bb=np.where(np.diff((X>0).astype(int))!=0)[0]
        if X[-1]>0:
            bb=np.concatenate((bb,[X.size-1]))
        if X[0]>0:
            bb=np.concatenate(([0],bb))
        self.band_bound=np.column_stack((bb[::2],bb[1::2]+1))
        self.numbands=len(self.band_bound)        
        if th_bw is not None:
            self.band_merge(th_bw)
        if th_h is not None:
            self.band_remove(th_h)
        if compute_stat|bands:
            self.bandstatsAll()
        if  bands:
            self.bandout()    
        #self.band_Area=np.array([np.trapz(X[np.arange(*b)]) for b in self.band_bound])
        #self.band_Max=np.array([np.max(X[np.arange(*b)]) for b in self.band_bound])
        #self.band_Max_loc=np.array([np.argmax(X[np.arange(*b)])+b[0] for b in self.band_bound])
        #self.d_band=self.band_bound[1:,0]-self.band_bound[:-1,1]
    
    def band_merge(self,thresh):
        bb=self.band_bound
        dd=bb[1:,0]-bb[:-1,1]
        while len(np.where(dd<thresh)[0])>0:
            d=np.where(dd<thresh)[0][0]
            nb=[bb[d][0],bb[d+1][1]]
            nbb=np.delete(bb,[d,d+1],axis=0)
            nbb=np.insert(nbb,d,nb,axis=0)
            bb=nbb
            dd=bb[1:,0]-bb[:-1,1]
        self.band_bound=bb
        self.numbands=len(self.band_bound)

    def band_remove(self,thresh):
        bb=self.band_bound
        bb_max=np.array([np.max(self.X[np.arange(*b)]) for b in self.band_bound])
        nbb=np.delete(bb,np.where(bb_max<thresh)[0],axis=0)
        self.band_bound=nbb

    def bandStats(self,b):
        return np.trapz(self.X[np.arange(*b)]),np.max(self.X[np.arange(*b)]),np.argmax(self.X[np.arange(*b)]) +b[0]
    def bandstatsAll(self):
        self.numbands=len(self.band_bound)
        self.band_Area,self.band_Max,self.band_Max_loc=[None]*3
        if self.numbands>0:
            self.band_Area,self.band_Max,self.band_Max_loc=np.array([self.bandStats(b) for b in self.band_bound]).T

    def bandout(self):
        #self.tst = Band(self.var,self.band_bound,self.band_Area,self.band_Max,self.band_Max_loc)
        #print(self.tst.var)
        self.bands=[]
        for i in range(self.numbands):
            self.bands.append(Band(self.var,self.band_bound[i],self.band_Area[i],self.band_Max[i],self.band_Max_loc[i]))



class Band():
    def __init__(self,variable,band,area,maxval,maxloc):
        self.variable = variable
        self.start = band[0]
        self.width = band[1]-band[0]
        self.loc = int(self.width/2)+ band[0]
        self.area = area
        self.max = maxval
        self.max_loc = maxloc

def maxtracksfromavg(allwindowalltracks,maxargs,threshold):
    return np.array([fp.Track(allwindowalltracks[e][maxargs[e]],e,maxargs[e],bands=True,th_bw=10,th_h=threshold) for e in range(len(maxargs))])

def gettracks(data,bandbool,bandwidth,height):
    return [Track(X,i,bands=bandbool,th_bw=bandwidth,th_h=height) for i,X in enumerate(data.T)]


def setupbandarray(tracks,):
    x=np.zeros(tracks[0].X.shape[0],dtype=bool)
    


def extract_loc_from_bands(track,bands):
    X=np.zeros(track.X.shape[0]).astype(bool)
    ind=[b.loc for b in bands]
    X[ind]=True
    return X

def extract_max_from_bands(track,bands):
    y=np.zeros(track.X.shape[0])
    ind=[b.loc for b in bands]
    m=[b.max for b in bands]
    y[ind]=m
    return y


def sets(pri,pci,bounds):
    A=np.unique(pri[np.where(pci<=bounds[0])[0]])
    B=np.unique(pri[np.where(pci>=bounds[1])[0]])
    C=np.unique(pri[np.where((pci>bounds[0])&(pci<bounds[1]))[0]])
    U=np.unique(np.concatenate((A,B,C)))
    return A,B,C,U

def insidebound(pri,pci,bounds):
    A=np.unique(pri[np.where(pci<=bounds[0])[0]])
    B=np.unique(pri[np.where(pci>=bounds[1])[0]])
    C=np.unique(pri[np.where((pci>bounds[0])&(pci<bounds[1]))[0]])
    U=np.unique(np.concatenate((A,B,C)))
    return np.setdiff1d(np.setdiff1d(U,A),B)

def bandsinrange(allt):
    t=np.array([len(a.bands) for a in allt])==0
    return ~t

def getbands(allt,iv):
    B=[a.bands for a in allt[iv]]
    return np.concatenate([[[i.variable,i.loc] for i in ban] for ban in B])

def plotinrange(lower,upper,allt,bands):
    print(f'[plot(allt[b[0]].X) for b in bands if (b[1]>={lower}) & (b[1]<={upper})]')

def tracksinrange(bands,allt,iv,lower,upper,maxval=None):
    B=[a.bands for a in allt[iv]]
    I=np.concatenate([[[i.variable,i.max_loc,i.max] for i in ban] for ban in B])
    if maxval is not None:
        return np.array([b[0] for b in I if ((b[1]>lower) & (b[1]<upper)) & (b[2]>maxval)]).astype(int)
    return np.array([b[0] for b in I if (b[1]>lower) & (b[1]<=upper)]).astype(int)


