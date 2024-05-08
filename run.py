import os
import sys
import numpy as np
sys.path.append('/home/bmanookian/Timescan/')
import data_loader as dataload
import scanrun as sr
import scananalysis as sa
import trackanalysis as ta

# inputs - Change below here as needed
deltawindow=300
nprocs=28
thresh=0.01

# take inputs
dotfile=sys.argv[1]
datafile=sys.argv[2]


## CODE BELOW SHOULD NOT BE CHANGED ##
 
# prepare output folder for scan scores output
folder_name = 'masterscan'
if not os.path.exists(folder_name):
	os.makedirs(folder_name)
else:
	print(f"Folder '{folder_name}' already exists.")

#outputdir=os.path.join(workdir, folder_name)	


# Load Data from input
data,labels=dataload.getdataandlabels(datafile)

#Setup time run
timescan=sr.Scan(data,labels,dotfile,deltawindow)

# save nodes and edge files
np.save('nodenames.npy',timescan.nodes)
np.save('edgenames.npy',timescan.edges)


### Run scan and save to masterscan output ###

sr.scanandsave(timescan,nprocs)

print('Scores files saved to: masterscan/')



# Heatmap calculation
print('Moving to heatmap calculation')
# Load output files from masterscan
out = [np.load(f'./masterscan/scores_{i}.npy') for i in timescan.windowlist]

# Build heatmap for run

scan=sa.Scandot(out,timescan.windowlist,timescan.data.shape[1])
dotout=[scan.allwinalledge(j) for j in range(len(timescan.windowlist))]
heatmap=scan.converttoheatmap(dotout)

# Save to output file
print(f'Heatmap completed with shape {heatmap[:,:,:-1].shape}')
np.save('heatmap.npy',heatmap[:,:,:-1])


# Below provides numpys to be used for analysis via trackanalysis.py

T,iv=ta.getT(thresh,heatmap=heatmap[:,:,:-1],windows=1)

np.save('tracks.npy',T)
np.save('edges_abv_cutoff.npy',iv)

