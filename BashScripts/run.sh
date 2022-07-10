#!/bin/bash
#./initialize.sh
cd ..

### Data Generation ###

### DREAM4 
# echo "Running config_dream4_10\n"
# DONE python BLRunner.py --config config-files/config_dream4_10.yaml
# DONE python BLEvaluator.py --config config-files/config_dream4_10.yaml -a -u -j -n -z -y -t -e -x
#!! Run with elapsed time -> python BLEvaluator.py --config config-files/config_dream4_10.yaml -t

# echo "Running config_dream4_100\n"
# DONE python BLRunner.py --config config-files/config_dream4_100.yaml
# DONE python BLEvaluator.py --config config-files/config_dream4_100.yaml -a -u -j -n -z -y -t -e -x
#!! Run with elapsed time -> python BLEvaluator.py --config config-files/config_dream4_100.yaml -t

#--------------------------------------------------------------------#
#--------------------------------------------------------------------#

### SERGIO BULK
# echo "Running config_sergio_bulk_100\n"
# DONE python BLRunner.py --config config-files/config_sergio_bulk_100.yaml
# DONE python BLEvaluator.py --config config-files/config_sergio_bulk_100.yaml -a -u -j -n -z -y -t -e -x
# !!Run with elapsed time -> python BLEvaluator.py --config config-files/config_sergio_bulk_100.yaml -t

# echo "Running config_sergio_bulk_400\n"
# DONE python BLRunner.py --config config-files/config_sergio_bulk_400.yaml
python BLEvaluator.py --config config-files/config_sergio_bulk_400.yaml -a -u -j -n -z -y -t -e -x
# ORDER_MCMC about 16 hours - 16*15h = 240h = 10d
# GENENET - 6:41:10

# echo "Running config_sergio_bulk_1200\n"
# DONE python BLRunner.py --config config-files/config_sergio_bulk_1200.yaml
python BLEvaluator.py --config config-files/config_sergio_bulk_1200.yaml -a -u -j -n -z -y -t -e -x


#--------------------------------------------------------------------#
#--------------------------------------------------------------------#

### SERGIO FULL
echo "Running config_sergio_100\n"
# DONE python BLRunner.py --config config-files/config_sergio_100.yaml
python BLEvaluator.py --config config-files/config_sergio_100.yaml -a -u -j -n -z -y -t -e -x
# ORDER_MCMC - more than a day
# PC - more than 8 hours

echo "Running config_sergio_400\n"
python BLRunner.py --config config-files/config_sergio_400.yaml

# echo "Running config_sergio_1200\n"
# python BLRunner.py --config config-files/config_sergio_1200.yaml

#--------------------------------------------------------------------#
#--------------------------------------------------------------------#

### TCGA
# echo "Running config_tcga"
# python BLRunner.py --config config-files/config_tcga.yaml
