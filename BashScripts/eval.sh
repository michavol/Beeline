#!/bin/bash
cd ..
echo "Evaluating config_dream4_10\n"
python BLEvaluator.py --config config-files/config_dream4_10.yaml $1 #-a # -u -j -r -e #-t #-p #-m  #-b
#python BLEvaluator.py --config config-files/config_dream4_10.yaml -a -u -j -n -z -y -t -e -x

# echo "Evaluating config_dream4_100\n"
# $python BLEvaluator.py --config config-files/config_dream4_100.yaml $1 #-a # -u -j -r -e #-t #-p #-m  #-b
#python BLEvaluator.py --config config-files/config_dream4_100.yaml -a -u -j -n -z -y -t -e -x

#echo "Evaluating config_sergio_bulk_100\n"
# python BLEvaluator.py --config config-files/config_sergio_bulk_100.yaml $1 #-a # -u -j -r -e #-t #-p #-m  #-b
#python BLEvaluator.py --config config-files/config_sergio_bulk_100.yaml -a -u -j -n -z -y -t -e -x

#echo "Evaluating config_sergio_100\n"
# python BLEvaluator.py --config config-files/config_sergio_100.yaml $1 #-a # -u -j -r -e #-t #-p #-m  #-b

#echo "Evaluating config_sergio_400\n"
# python BLEvaluator.py --config config-files/config_sergio_400.yaml $1 #-a # -u -j -r -e #-t #-p #-m  #-b

#echo "Evaluating config_sergio_bulk_400\n"
# python BLEvaluator.py --config config-files/config_sergio_bulk_400.yaml $1 #-a # -u -j -r -e #-t #-p #-m  #-b

#echo "Evaluating config_sergio_1200\n"
# python BLEvaluator.py --config config-files/config_sergio_1200.yaml $1 #-a # -u -j -r -e #-t #-p #-m  #-b

#echo "Evaluating config_sergio_bulk_1200\n"
# python BLEvaluator.py --config config-files/config_sergio_bulk_1200.yaml $1 #-a # -u -j -r -e #-t #-p #-m  #-b
