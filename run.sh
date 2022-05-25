#!/bin/bash
./initialize.sh

python BLRunner.py --config config-files/config.yaml
#python BLRunner.py --config config-files/config_example.yaml
#python BLEvaluator.py --config config-files/config.yaml -a
#python BLEvaluator.py --config config-files/config_example.yaml -a
#python BLEvaluator.py --help