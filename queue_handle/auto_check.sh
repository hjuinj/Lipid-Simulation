#!/bin/sh

#PBS -l walltime=71:59:00
#PBS -l select=1:ncpus=1
#PBS -N Queue_Patrol

module load intel-suite
module load mpi
module load python/2.7.3



COUNTER=0
INTERVAL=$((60 * 15))  #15 mins
LIMIT=$((60 * 60 * 48)) #48 hrs
while true
do 
    $HOME/Scripts/exe/pupdate.py 
    #echo "updated"
    sleep $INTERVAL 
    COUNTER=$[$COUNTER + $INTERVAL]
    if  [ $COUNTER -eq  $LIMIT ];
    then 
        qdel $PBS_JOBID
        qsub -e /dev/null -o /dev/null $HOME/Scripts/auto_check.sh 
	#echo "submitted"
        break
    fi
done
