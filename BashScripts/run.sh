#!/bin/bash
cd ..

#echo "Running config_tcga"
#python BLRunner.py --config config-files/config_tcga.yaml

echo "Running config_dream4\n"
python BLRunner.py --config config-files/config_dream4.yaml $1 #-a # -u -j -r -e #-t #-p #-m  #-b

# echo "Running config_sergio_bulk_100\n"
# python BLRunner.py --config config-files/config_sergio_bulk_100.yaml $1 #-a # -u -j -r -e #-t #-p #-m  #-b

# echo "Running config_sergio_100\n"
# python BLRunner.py --config config-files/config_sergio_100.yaml $1 #-a # -u -j -r -e #-t #-p #-m  #-b

# echo "Running config_sergio_400\n"
# python BLRunner.py --config config-files/config_sergio_400.yaml $1 #-a # -u -j -r -e #-t #-p #-m  #-b

# echo "Running config_sergio_bulk_400\n"
# python BLRunner.py --config config-files/config_sergio_bulk_400.yaml $1 #-a # -u -j -r -e #-t #-p #-m  #-b

#echo "Running config_sergio_1200\n"
# python BLRunner.py --config config-files/config_sergio_1200.yaml $1 #-a # -u -j -r -e #-t #-p #-m  #-b

#echo "Running config_sergio_bulk_1200\n"
# python BLRunner.py --config config-files/config_sergio_bulk_1200.yaml $1 #-a # -u -j -r -e #-t #-p #-m  #-b
