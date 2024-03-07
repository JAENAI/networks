#!/bin/bash

echo "Starting scenario 2 ..."

TIMEOUTS=(0.05 0.1)
BUFFER_SIZES=(16384 32768)
PROBABILITIES=(0.05 0.1 0.15 0.2 0.3 0.4)
WINDOWS=(2 6)
PROCESSES=10
FILES=1

for i in ${TIMEOUTS[@]}
do
    for j in ${BUFFER_SIZES[@]}
    do
        for k in ${PROBABILITIES[@]}
        do 
            for l in ${WINDOWS[@]}
            do
                start=$(date +%s)
                python3 main.py --server $PROCESSES $1 $k $i $j $l $FILES &
                server_pid=$!
                python3 main.py --clients $PROCESSES $1 $j $l $FILES &
                client_pid=$!

                wait $server_pid
                wait $client_pid
                end=$(date +%s)
                taken=$((end-start))
                echo "timeout: $i buffer: $j prob: $k window: $l time: $taken" >> log1.txt
            done
        done
    done
done