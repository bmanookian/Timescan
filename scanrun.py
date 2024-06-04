import numpy as np
import pygraphviz as pgv
import multiprocessing
import entropy as en

# parallel function
def runParallel(foo,iter,ncore):
    pool=multiprocessing.Pool(processes=ncore)
    try:
        out=(pool.map_async( foo,iter )).get()  
    except KeyboardInterrupt:
        print ("Caught KeyboardInterrupt, terminating workers")
        pool.terminate()
        pool.join()
    else:
        #print ("Quitting normally core used ",ncore)
        pool.close()
        pool.join()
    try:
        return out
    except Exception:
        return out



# get edges from the rendering file

def getedgefromdot(dotfile,moralize=False):
    G=pgv.AGraph(dotfile)
    nodes=np.sort(np.array(G.nodes()))
    if moralize==True:
        import networkx as nx
        mG=nx.moral_graph(nx.nx_agraph.from_agraph(G))
        edges=np.array([e[0]+'->'+e[1] for e in np.array(list(mG.edges()))])
        return nodes,edges
    edges=np.array([e[0]+'->'+e[1] for e in  np.array(G.edges())])
    return nodes,edges

# Possibly put a test here that makes sure the number of labels in the data 
# file matches that in the rendering file



# create library(dictionary) for labels(nodes)
def getlabdict(nodes):
    labdict={}
    for index,element in enumerate(nodes):
        labdict[element]=index
    return labdict

# Create enumerated edges array

def edgeenumerate(edgenames,labdict):
    edgesplit=np.array([i.split('->') for i in edgenames])
    return np.array([[labdict[i],labdict[j]] for i,j in edgesplit])


# MI Scan function and class that takes as input data and enumerated edges
def miScan(data,edgenums,w):
    return [en.mi_p([data[i][w[0]:w[1]],data[j][w[0]:w[1]]]) for i,j in edgenums]

# At this stage we can take as input the windows with wich you want to scan

def createwindowslist(window,datamax):
    return np.arange(150,datamax-window,window)

# create the scanning windows

def getscanWindows(datamax,window,shift):
    x=np.arange(0,datamax-window,shift)
    y=x+window
    return np.column_stack([x,y])

class Scan():
    def __init__(self,data,labels,dotfile,deltawindow=300,windowlist=None):
        # get edges and nodes and enumerate edges
        self.nodes,self.edges=getedgefromdot(dotfile)
        self.data=data[np.in1d(labels,self.nodes)]
        self.datamax=self.data.shape[1]
        self.nodedict=getlabdict(self.nodes)
        print(self.data.shape,self.nodes.shape,self.edges.shape)
        self.edgenums=edgeenumerate(self.edges,self.nodedict)

        # Prepare windows list 
        self.windowlist=windowlist
        if windowlist is None:
            self.windowlist=createwindowslist(deltawindow,self.datamax)

    def scores(self,window):
        return miScan(self.data,self.edgenums,window)

def scanandsave(scan,nprocs,scoresdir='./masterscan/'):

    for i,window in enumerate(scan.windowlist):
        W=getscanWindows(scan.datamax,window,shift=1)
        out=np.array(runParallel(scan.scores,W,nprocs))
        np.save(scoresdir+f'scores_{window}.npy',out.T)
        print(f'Scores_{window} written')
    return        
            
    
            

