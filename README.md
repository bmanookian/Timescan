# Timescan

This folder contains all the codes required to run the timescan algorithm.


Required Inputs are:

1. rendered dot file output from BN calculation
2. csv data file in format row-based with first low as feature labels

To Run using submit file:
in submit file run as follows

python run.py DOTFILE DATACSVFILE



other options can be changed in run python file as needed:

    provide the number of processors you would like to use (nprocs)

    provide the windows you want to use
    example: 300 would scan using windows starting at 150 and moving by 300
             -> 150,450,750, etc

Once all inputs are complete you can use the submit file to submit to cluster.

Output from this will be:

a folder names 'masterscan' that contains a numpy file for each window scan

multiple files
1. edgenames and nodenames numpys extracted from the BN
2. a heatmap file created from all the scores - this can be used in the final step to give complete output of tracks for all edges


