# Autonomous Driving Ethics in the CommonRoad Platform

The above repository is adapted from the CommonRoad Search platform for evaluating scenarios. It includes additional processing functions to empirically determine the safety and ethical capabilities of planners and solved scenarios. Currently, the tool is only compatible with planners employing the BestFirstSearch algorithm but will be expanded upon. Steps to use are as follows.

1. Set up the commonroad docker: first clone the commonroad-search repository (https://gitlab.lrz.de/tum-cps/commonroad-search/-/tree/master/) and then follow the instructions in the docker subdirectory
2. Replace the commonroad-search subdirectory with this repository
3. Copy any scenarios you want to test into the commonroad-scenarios-master subdirectory. Currently it contains the dilemma scenario used for ethical analysis.
4. In SMP --> motion_planner --> student.py, replace this algorithm with any planner that also employs the BestFirstSearch algorithm.
5. In tutorials --> batch_processing, run the script to generate solutions for your planner. 
6. In outputs --> processing, run the scripts to generate data for the solutios found.
