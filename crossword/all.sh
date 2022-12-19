#!/bin/bash

str='python generate.py data/structure'
str2='.txt data/words'
str3='.txt'

for (( i=2; i>-1; i-- ))
do
    for (( j=2; j>-1; j-- ))
    do
        echo 'Working on: structure'$i' words'$j
        $str$i$str2$j$str3
        echo -e '\n'
    done
    echo -e '\n'
done
