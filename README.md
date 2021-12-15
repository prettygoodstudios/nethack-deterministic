# Deterministic NetHack Algorithm

* The main file in this repository is [Agent.py](./Agent.py). Running this script will run the algorithm on a randomly generated dungeon and will print the game's state to the screen after each move taken by the agent. The algorithm will quit, when it either dies or reaches the staircase.

* The dependencies to install are matplotlib, nle and gym. These can all be installed with pip `pip3 install matplotlib nle gym`. This program must be run with python 3.5+ due to its use of some more recent python features.

## Running Effectiveness Study

* The effectiveness study can be run by running the following bash script [batchrunner.sh](./batchrunner.sh). This will run 300 trials and will output the results to `batchrun.txt`. 

* It logs all of the renders in addition to the results so this file can reach about half a Gigabyte. The script can be interrupted partially through to run fewer trials.

* If you are interested in only seeing the result of each trial, you can grep the output in the following way `grep Result: batchrun.txt`. The first value is the success/failure of the trial, the second value is the length of the optimal path and the third value is the length of the path actually taken by the algorithm.
