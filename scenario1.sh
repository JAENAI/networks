#!/bin/bash

echo "Starting scenario 1 ..."

TIMEOUTS=(0.1)
BUFFER_SIZE=32768
PROBABILITIES=(0.05 0.1 0.15 0.2 0.3)
WINDOWS=(2 6)
PROCESSES=2
FILES=1

for i in ${TIMEOUTS[@]}
do
    for k in ${PROBABILITIES[@]}
    do 
        for l in ${WINDOWS[@]}
        do
            start=$(date +%s)
            python3 main.py --server $PROCESSES $1 $k $i $BUFFER_SIZE $l $FILES &
            server_pid=$!
            python3 main.py --clients $PROCESSES $1 $BUFFER_SIZE $l $FILES &
            client_pid=$!

            wait $server_pid
            wait $client_pid
            end=$(date +%s)
            taken=$((end-start))
            echo "timeout: $i buffer: $BUFFER_SIZE prob: $k window: $l time: $taken" >> log.txt
        done
    done
done


