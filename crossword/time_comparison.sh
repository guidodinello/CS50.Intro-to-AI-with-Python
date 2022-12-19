#!/bin/bash

runned_times=200

while true; do
    start=$SECONDS

for (( i=0 ; i<runned_times; i++ ))
do
    python generate.py data/structure2.txt data/words2.txt
done


    duration=$(( SECONDS - start ))
    division=$duration/$runned_times
    echo "This script took an average of $duration seconds per run"
    if true; then break; fi
done
