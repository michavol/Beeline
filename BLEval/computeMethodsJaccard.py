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

def MethodsJaccard(dataDict, inputSettings, undirected = False):
    """
    A function to compute median pairwirse Jaccard similarity index
    of predicted top-k edges for a given set of datasets (obtained from
    the same reference network). Here k is the number of edges in the
    reference network (excluding self loops). 
    
    
    :param evalObject: An object of class :class:`BLEval.BLEval`.
    :type evalObject: :obj:`BLEval`
      
      
    :param datasetName: Name of the dataset for which the across method Jaccard index is computed.
    :type datasetName: str
      
      
    :returns:
        - median: Median of Jaccard correlation values
        - mad: Median Absolute Deviation of  the Spearman correlation values
    """

    ### Read file and get number of true edges
    headerList = ['Gene1', 'Gene2', 'Type']
    trueEdgesDF = pd.read_csv(str(inputSettings.datadir)+'/'+ dataDict['name'] +
                                '/' +dataDict['trueEdges'],
                                sep = '\t', 
                                header = 0, index_col = None)
    
    trueEdgesDF.columns = headerList
    trueEdgesDF = trueEdgesDF[trueEdgesDF["Type"] != 0]
    numEdges = len(trueEdgesDF)

    ### Initialize jaccard dictionary
    JACCARD = {}
    rankDict = {}

    ### Set-up outDir that stores output directory name
    outDir = "outputs/"+str(inputSettings.datadir).split("inputs/")[1]+ '/' +dataDict['name']
    
    ### Define swap function for undirected jaccard index
    def swap(genes):
        if int(genes[0][1:]) < int(genes[1][1:]):
            return [genes[0],genes[1]]
        else:
            return [genes[1],genes[0]]


    
    for algo1_index, algo1 in enumerate(inputSettings.algorithms):
     
        # check if the output rankedEdges file exists
        if Path(outDir + '/' +algo1[0]+'/rankedEdges.csv').exists():
            # Read predicted network
            predDF1 = pd.read_csv(outDir + '/' +algo1[0]+'/rankedEdges.csv', \
                                        sep = '\t', header =  0, index_col = None)
            
            # Extract first k-edges
            if (len(predDF1 > numEdges)):
                predDF1 = predDF1.iloc[:numEdges,:]

            # Order gene names if undirected
            if (undirected == True):
                predDF1.loc[:,["Gene1","Gene2"]] = predDF1.loc[:,["Gene1","Gene2"]].apply(swap,1,result_type='broadcast')

            # Define set of edges
            if (len(predDF1) > 0):
                rankDict1 = set(predDF1['Gene1'] + "|" + predDF1['Gene2'])
            else:
                rankDict1 = set([])
            
            # Iterate through all other algorithms
            for algo2_index, algo2 in enumerate(inputSettings.algorithms):
                # skip algorithm if the pair has already been checked
                # if (algo2_index<algo1_index):
                #     continue

                # check if the output rankedEdges file exists
                if Path(outDir + '/' +algo2[0]+'/rankedEdges.csv').exists():
            
                    # Read predicted network
                    predDF2 = pd.read_csv(outDir + '/' +algo2[0]+'/rankedEdges.csv', \
                                                sep = '\t', header =  0, index_col = None)

                    # Extract first k-edges
                    if (len(predDF2 > numEdges)):
                        predDF2 = predDF2.iloc[:numEdges,:]

                    # Order gene names if undirected
                    if (undirected == True):
                        predDF2.loc[:,["Gene1","Gene2"]] = predDF2.loc[:,["Gene1","Gene2"]].apply(swap,1,result_type='broadcast')

                    # Define set of edges
                    if (len(predDF2) > 0):
                        rankDict2 = set(predDF2['Gene1'] + "|" + predDF2['Gene2'])
                    else:
                        rankDict2 = set([])

                    # Compute Jaccard index
                    num = len(rankDict1.intersection(rankDict2))
                    den = len(rankDict1.union(rankDict2))
                    if den != 0:
                        jaccIndex = num/den
                    else:
                        jaccIndex = 0

                    JACCARD[algo1[0] + "-" + algo2[0]] = jaccIndex

                else:
                    print(outDir + '/' +algo2[0]+'/rankedEdges.csv', ' does not exist. Skipping...')

        else:
            print(outDir + '/' +algo1[0]+'/rankedEdges.csv', ' does not exist. Skipping...')
            
    return JACCARD
