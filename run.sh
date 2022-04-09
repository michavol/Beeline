#!/bin/bash
./initialize.sh

python BLRunner.py --config config-files/config.yaml
#python BLEvaluator.py --config config-files/config.yaml --auc
#python BLEvaluator.py --help