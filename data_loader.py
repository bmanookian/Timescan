import numpy as np

class proteindata():
    def __init__(self,input_csv):
        self.csv_data = np.loadtxt(input_csv,delimiter=',',dtype=str)
        self.input_data = self.csv_data[1:].astype(float).astype(int).T
        self.input_length = len(self.input_data)
        self.input_labels = self.csv_data[0]
        self.labels = [] 
        self.singles = len(np.array([i for i in self.input_data if i[0] == np.all(i)]))

    def shrink(self,batch,length=None):
        if batch == 'all':
            self.data = self.input_data
        if batch == 1:
            self.data = self.input_data[:,:length]
        if batch == 2:
            self.data = self.input_data[:,length:2*length]
        if batch == 3:
            self.data = self.input_data[:,2*length:3*length]
        if batch == 4:
            self.data = self.input_data[:,3*length:4*length]
        if batch == 5:
            self.data = self.input_data[:,4*length:5*length]
        
    def randomize(self):
        for i in range(len(self.data)):
            self.data[i] = np.random.permutation(self.data[i])
    
        

def getdataandlabels(inp,removesingles=False):
    protein=proteindata(inp)
    protein.shrink('all')
    if removesingles:
        print(protein.data.shape[0])
        protein.remove_single_state()
        print(protein.data.shape[0])
        return protein.data,np.array(protein.labels)
    return protein.data,np.array(protein.input_labels)


