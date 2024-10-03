import os
import sys
import numpy as np
import pickle
sys.path.append('/home/bmanookian/Timescan/')
import data_loader as dataload
import scanrun as sr
import scananalysis as sa

# inputs - Change below here as needed
deltawindow=300
nprocs=28
windowlist=[150,450,750,1050]


## CODE BELOW SHOULD NOT BE CHANGED ##

# take inputs
dotfile=sys.argv[1]
datafile=sys.argv[2]
 
# prepare output folder for scan scores output
folder_name = 'masterscan'
if not os.path.exists(folder_name):
	os.makedirs(folder_name)
else:
	print(f"Folder '{folder_name}' already exists.")


# Load Data from input
data,labels=dataload.getdataandlabels(datafile)

#Setup time run
dbn=sr.Scan(data,labels,dotfile,deltawindow,windowlist)

# save nodes and edge files
np.save('nodenames.npy',dbn.nodes)
np.save('edgenames.npy',dbn.edges)


### Run scan and save to masterscan output ###

sr.scanandsave(dbn,nprocs)

print('Scores files saved to: masterscan/')



# Heatmap calculation
print('Moving to heatmap calculation')
# Load output files from masterscan
out = [np.load(f'./masterscan/scores_{i}.npy') for i in dbn.windowlist]

# Build heatmap for run

scan=sa.Scandot(out,dbn.windowlist,dbn.data.shape[1])
dotout=[scan.allwinalledge(j) for j in range(len(dbn.windowlist))]
heatmap=scan.converttoheatmap(dotout)

# Save to output file
print(f'Heatmap completed with shape {heatmap[:,:,:-1].shape}')
np.save('heatmap.npy',heatmap[:,:,:-1])


# Below provides numpys to be used for analysis via trackanalysis.py

allt,iv,events,maxargs=sa.getalltivandevents(0.01,windows=None)

#Complete dbn object and save to pickel file
dbn.settracks(np.array([allt[i].X for i in range(len(allt))]))
dbn.computewd()
with open('dbn.pkl', 'wb') as file:
    pickle.dump(dbn, file)

np.save('tracks.npy',dbn.tracks)
np.save('tracks_cutoff.npy',iv)
np.save('events.npy',events)
