import numpy as np
import networkx as nx
import sys
sys.path.append('/home/bmanookian/Timescan/')


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


# degree and betweenness
def initgraph(nodes):
    G=nx.DiGraph()
    G.add_nodes_from(nodes)
    return G

def getevals(T,t):
    evals=np.copy(T[:,t])
    return evals

def addedges(G,edges,evals,thresh):
    G.add_edges_from(edges[evals>thresh])
    return G

def clear_edges(G):
    return nx.create_empty_copy(G)

def get_Degree(G):
    return np.array(list(nx.degree_centrality(G).values()))

def get_Between(G):
    return np.array(list(nx.betweenness_centrality(G).values()))

class Scan():
    def __init__(self,edges,nodes,T,thresh=0.01):
        self.edges=edges
        self.nodes=nodes
        self.T=T
        self.Tmax=T.shape[1]
        self.thresh=thresh

        #Make windows
        x=np.arange(0,T.shape[1],300)
        y=x+300
        self.W=np.column_stack((x,y))[:-1]

    def deg_bet_t(self,t):
        iG=initgraph(self.nodes)
        self.G=addedges(iG,self.edges,getevals(self.T,t),self.thresh)
        D=get_Degree(self.G)
        B=get_Between(self.G)
        return np.array([D,B])
    
    def deg_bet_deltat(self,window):
        return np.array([self.deg_bet_t(t) for t in np.arange(window[0],window[1])])

#out=par.runParallel(scan.deg_bet_deltat,scan.W,25)#
