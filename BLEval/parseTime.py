import os
import argparse
import numpy as np
import pandas as pd
import networkx as nx
from tqdm import tqdm
import multiprocessing
from pathlib import Path
import concurrent.futures
from itertools import permutations
from collections import defaultdict
from multiprocessing import Pool, cpu_count
from networkx.convert_matrix import from_pandas_adjacency

def getTime(evalObject, dataset, measurement):
    """
    Return time taken for each of the algorithms
    in the evalObject on the dataset specified.
    The output stored in time.txt is parsed to
    obtain the CPU time.

    :param evalObject:   An object of the class :class:`BLEval.BLEval`
    :type evalObject: BLEval
    :param dataset:   Dataset name for which the time output must be parsed for each algorithm.
    :type dataset: str
      
    
    :returns: 
        A Dictionary of time taken by each of the algorithms, i.e., key is the algorithm name, and
        value is the time taken (in sec.).

    """

    
    # Set the output directory for a given dataset 
    # where the time.txt files are stored for each algorithm.
    outDir = str(evalObject.output_settings.base_dir) + \
             str(evalObject.input_settings.datadir).split("inputs")[1] + "/" + dataset["name"] + "/"
    
    # Initialize algorithm:time-taken dictionary
    algo_dict = dict()
    
    # Obtain the list of algorithms for which the 
    # time.txt files must be read in the outDir
    algos = evalObject.input_settings.algorithms
    
    # Repeat for each algorithm
    for algo in tqdm(algos, 
                        total = len(algos), unit = " Algorithms"):
    #for algo in algos:
        # Check if single time.txt file
        path = outDir+algo[0]+"/time.txt"

        #print("This is the path: " + path)
        if Path(path).exists():
            # If so, parse the time.txt file
            # to obtain CPU time taken to run the
            # GRN algorithm on the given dataset
            time = parse_time_files(path, measurement)
        else:
            time = -1
        
        algo_dict[algo[0]] = time

    return algo_dict

def get_sec(time_str):
    """Get seconds from time."""
    if (len(time_str.split(':')) == 3):
        h, m, s = time_str.split(':')
        return float(h) * 3600 + float(m) * 60 + float(s)
    else:
        m, s = time_str.split(':')
        return float(m) * 60 + float(s)

def parse_time_files(path, measurement):
    """
    Return time taken for each of the algorithms
    in the evalObject on the dataset specified.
    The output stored in time.txt is parsed to
    obtain the CPU time.

    :param path: Path to the time.txt file, or timex.txt file where x corresponds to the trajectory ID for a given algorithm-dataset combination.
    :type path: str
      
    :returns: 
        A float value corresponding to the time taken.
         
    """
    try:
        with open(path, "r") as f:
            lines = f.readlines()

            if (measurement=="User"):
                line = lines[1]
                time_val = float(line.split()[-1])

            elif (measurement=="Elapsed"):
                line = lines[4]
                time_val = get_sec(line.split()[-1])

            elif (measurement=="CpuPercentage"):
                line = lines[3]
                time_val = float(line.split()[-1][:-1])
            
    # If file is not found, return -1.
    except FileNotFoundError:
        #print("Time output " +path+" file not found, setting time value to -1\n")
        time_val = -1
        
    # If file is present but the file is empty, return -1.
    except ValueError:
        #print("Algorithm running failed, setting time value to -1\n")
        time_val = -1

    return time_val
