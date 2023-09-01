#!/bin/bash
#This bash script will launch four parallel simulations from simulation_0.py, simulation_1.py, simulation_2.py, simulation_3.py
#The file ../files/TB_DIR_FILE.txt contains the list of all the testbenches to be simulated. Each line has the testbenchpath followed by space start time followed by space end time
#The script will create four folders job0, job1, job2, job3 in each testbench folder and copy all the files from the testbench folder to each of the job folders
#The script will then launch four parallel simulations from simulation_0.py, simulation_1.py, simulation_2.py, simulation_3.py
#The script will pass the testbench path, start time and end time as arguments to the simulations
#The script will then wait for all the simulations to complete
#The script will then launch the next four simulations
#The script will continue this process until all the simulations are complete

module add innovus
module add questasim/2018.10.7

while read TB START END; do
    echo $TB
    echo $START
    echo $END
    if [ -d $TB/job0 ]; then
        rm -rf $TB/job0
    fi
    if [ -d $TB/job1 ]; then
        rm -rf $TB/job1
    fi
    if [ -d $TB/job2 ]; then
        rm -rf $TB/job2
    fi
    if [ -d $TB/job3 ]; then
        rm -rf $TB/job3
    fi
    mkdir $TB/job0
    mkdir $TB/job1
    mkdir $TB/job2
    mkdir $TB/job3
    find $TB -maxdepth 1 -type f -exec cp {} $TB/job0 \;
    find $TB -maxdepth 1 -type f -exec cp {} $TB/job1 \;
    find $TB -maxdepth 1 -type f -exec cp {} $TB/job2 \;
    find $TB -maxdepth 1 -type f -exec cp {} $TB/job3 \;
    ITER_START_0=0
    ITER_END_0=50
    ITER_START_1=51
    ITER_END_1=100
    ITER_START_2=101
    ITER_END_2=150
    ITER_START_3=151
    ITER_END_3=201
    python3 simulation_0.py $TB $START $END $ITER_START_0 $ITER_END_0 &
    python3 simulation_1.py $TB $START $END $ITER_START_1 $ITER_END_1 &
    python3 simulation_2.py $TB $START $END $ITER_START_2 $ITER_END_2 &
    python3 simulation_3.py $TB $START $END $ITER_START_3 $ITER_END_3 &
done < ../files/TB_DIR_FILE.txt
