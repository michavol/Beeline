#!/bin/bash

cd ..

DATA_PATH=inputs/DREAM4 
cd $DATA_PATH

#Remove all generated folder in DREAM4 folder
find -name 'PPCOR' -exec rm -rf {} \;
find -name 'GENIE3' -exec rm -rf {} \;
find -name 'GRNBOOST2' -exec rm -rf {} \;
find -name 'MCMC' -exec rm -rf {} \;
find -name 'ORDER_MCMC' -exec rm -rf {} \;
find -name 'PARTITION_MCMC' -exec rm -rf {} \;
find -name 'TEST' -exec rm -rf {} \;
find -name 'PIDC' -exec rm -rf {} \;