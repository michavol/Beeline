#!/usr/bin/env python
# coding: utf-8

import os
import yaml
import argparse
import itertools
import numpy as np
import pandas as pd
import networkx as nx
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm
import multiprocessing
from pathlib import Path
import concurrent.futures
from itertools import permutations
from collections import defaultdict
from multiprocessing import Pool, cpu_count
from networkx.convert_matrix import from_pandas_adjacency

# local imports
import BLEval as ev 


def get_parser() -> argparse.ArgumentParser:
    '''
    :return: an argparse ArgumentParser object for parsing command
        line parameters
    '''
    parser = argparse.ArgumentParser(
        description='Run pathway reconstruction pipeline.')

    parser.add_argument('-c','--config', default='config.yaml',
        help="Configuration file containing list of datasets "
              "algorithms and output specifications.\n")
    
    parser.add_argument('-a', '--auc', action="store_true", default=False,
        help="Compute median of areas under Precision-Recall and ROC curves. Plot curves.\n")

    parser.add_argument('-u', '--auc_undirected', action="store_true", default=False,
        help="Compute median of areas under Precision-Recall and ROC curves for undirected inference. Plot curves\n")
    
    parser.add_argument('-j', '--jaccard', action="store_true", default=False,
      help="Compute median Jaccard index of predicted top-k networks "
      "for each algorithm for a given set of datasets generated "
      "from the same ground truth network.\n")

    parser.add_argument('-n', '--jaccard_undirected', action="store_true", default=False,
      help="Compute median Jaccard index of predicted top-k networks "
      "for each algorithm for a given set of datasets generated "
      "from the same ground truth network.\n")

    parser.add_argument('-z', '--jaccard_methods', action="store_true", default=False,
      help="Compute median Jaccard index of predicted top-k networks "
      "for each algorithm for a given set of datasets generated "
      "from the same ground truth network.\n")

    parser.add_argument('-y', '--jaccard_methods_undirected', action="store_true", default=False,
      help="Compute median Jaccard index of predicted top-k networks "
      "for each algorithm for a given set of datasets generated "
      "from the same ground truth network.\n")

    parser.add_argument('-r', '--spearman', action="store_true", default=False,
      help="Compute median Spearman Corr. of predicted edges "
      "for each algorithm  for a given set of datasets generated "
      " from the same ground truth network.\n")

    parser.add_argument('-t', '--time', action="store_true", default=False,
      help="Analyze time taken by each algorithm for a.\n")
    
    parser.add_argument('-e', '--epr', action="store_true", default=False,
      help="Compute median early precision.")

    parser.add_argument('-x', '--epr_undirected', action="store_true", default=False,
      help="Compute median early precision.")
    
    parser.add_argument('-s','--sepr', action="store_true", default=False,
      help="Analyze median (signed) early precision for activation and inhibitory edges.")

    parser.add_argument('-m','--motifs', action="store_true", default=False,
      help="Compute network motifs in the predicted top-k networks.")
    
    parser.add_argument('-p','--paths', action="store_true", default=False,
      help="Compute path length statistics on the predicted top-k networks.")

    parser.add_argument('-b','--borda', action="store_true", default=False,
      help="Compute edge ranked list using the various Borda aggregatio methods.")
        
    return parser

def parse_arguments():
    '''
    Initialize a parser and use it to parse the command line arguments
    :return: parsed dictionary of command line arguments
    '''
    parser = get_parser()
    opts = parser.parse_args()
    
    return opts

def main():
    opts = parse_arguments()
    config_file = opts.config

    evalConfig = None

    with open(config_file, 'r') as conf:
        evalConfig = ev.ConfigParser.parse(conf)
        
    print('\nPost-Run Evaluation:\n')
    evalSummarizer = ev.BLEval(evalConfig.input_settings, evalConfig.output_settings)
    
    outDir = str(evalSummarizer.output_settings.base_dir) + \
            str(evalSummarizer.input_settings.datadir).split("inputs")[1] + "/"+\
            str(evalSummarizer.output_settings.output_prefix) + "-"
    
    # Compute and plot ROC, PRC and report median AUROC, AUPRC    
    if (opts.auc):
        print("==="*30)
        print('Computing areas under ROC and PR curves (directed)...')
        print("==="*30)
        AUPRC, AUROC = evalSummarizer.computeAUC(directed=True)
        AUPRC['Mean AUPRC'] = AUPRC.mean(axis=1)
        AUPRC['Mean AUROC'] = AUROC.mean(axis=1)
        AUPRC['Std AUPRC'] = AUPRC.std(axis=1)
        AUPRC['Std AUROC'] = AUROC.std(axis=1)

        AUPRC.to_csv(outDir+'AUPRC_directed.csv')
        AUROC.to_csv(outDir+'AUROC_directed.csv')


    # Compute and plot ROC, PRC and report median AUROC, AUPRC for undirected inference  
    if (opts.auc_undirected):
        print("==="*30)
        print('Computing areas under ROC and PR curves (undirected)...')
        print("==="*30)
        AUPRC, AUROC = evalSummarizer.computeAUC(directed=False)
        AUPRC['Mean AUPRC'] = AUPRC.mean(axis=1)
        AUPRC['Mean AUROC'] = AUROC.mean(axis=1)
        AUPRC['Std AUPRC'] = AUPRC.std(axis=1)
        AUPRC['Std AUROC'] = AUROC.std(axis=1)

        AUPRC.to_csv(outDir+'AUPRC_undirected.csv')
        AUROC.to_csv(outDir+'AUROC_undirected.csv')
    
    
    # Compute directed Jaccard index across datasets  
    if (opts.jaccard):
        print("==="*30)
        print('Computing Jaccard index...')
        print("==="*30)

        jaccDict = evalSummarizer.computeJaccard(undirected=False, across_methods=False)
        jaccDict.to_csv(outDir + "Jaccard_directed.csv")


    # Compute undirected Jaccard index across datasets
    if (opts.jaccard_undirected):
        print("==="*30)
        print('Computing Jaccard index...')
        print("==="*30)

        jaccDict = evalSummarizer.computeJaccard(undirected=True)
        jaccDict.to_csv(outDir + "Jaccard_undirected.csv")


    # Compute directed Jaccard index across methods 
    if (opts.jaccard_methods):
        print("==="*30)
        print('Computing Jaccard index...')
        print("==="*30)

        jaccDict = evalSummarizer.computeMethodsJaccard(undirected=False)
        jaccDict["Mean Methods Jaccard"] = jaccDict.mean(axis=1)
        jaccDict["Std Methods Jaccard"] = jaccDict.std(axis=1)
        jaccDict.to_csv(outDir + "Jaccard_methods_directed.csv")

        #Generate mean jaccard matrix and plot heatmap
        jaccDict['AlgoPairs'] = jaccDict.index
        algoSplit = jaccDict["AlgoPairs"].str.split('-', expand = True)
        jaccDictSplit = pd.concat([algoSplit, jaccDict["Mean Methods Jaccard"]], axis=1)
        jaccDictSplit.columns = ["Algo1","Algo2","Jaccard"]

        jaccMat = jaccDictSplit.pivot(index='Algo1', columns='Algo2', values='Jaccard')
        triu = np.triu(np.ones_like(jaccMat), k=1)

        fig, ax = plt.subplots(figsize=(12, 12))
        sns.heatmap(jaccMat, annot=True, mask=triu, linewidths=.3)
        fig.savefig(outDir + "Jaccard_methods_directed_heatmap.png")


    # Compute undirected Jaccard index across methods 
    if (opts.jaccard_methods_undirected):
        print("==="*30)
        print('Computing Jaccard index...')
        print("==="*30)

        jaccDict = evalSummarizer.computeMethodsJaccard(undirected=True)
        jaccDict["Mean Methods Jaccard"] = jaccDict.mean(axis=1)
        jaccDict["Std Methods Jaccard"] = jaccDict.std(axis=1)
        jaccDict.to_csv(outDir + "Jaccard_methods_undirected.csv")

        #Generate mean jaccard matrix and plot heatmap
        jaccDict['AlgoPairs'] = jaccDict.index
        algoSplit = jaccDict["AlgoPairs"].str.split('-', expand = True)
        jaccDictSplit = pd.concat([algoSplit, jaccDict["Mean Methods Jaccard"]], axis=1)
        jaccDictSplit.columns = ["Algo1","Algo2","Jaccard"]

        jaccMat = jaccDictSplit.pivot(index='Algo1', columns='Algo2', values='Jaccard')
        triu = np.triu(np.ones_like(jaccMat), k=-1)

        fig, ax = plt.subplots(figsize=(12, 12))
        sns.heatmap(jaccMat, annot=True, mask=triu, linewidths=.3)
        fig.savefig(outDir + "Jaccard_methods_undirected_heatmap.png")

        
    # Compute Spearman correlation scores
    if (opts.spearman):
        print("\n\n" + "==="*30)
        print('Computing Spearman\'s correlation...')
        print("==="*30)
        corrDict = evalSummarizer.computeSpearman()
        corrDict.to_csv(outDir + "Spearman.csv")
      
        
    # Compute median time taken
    if (opts.time):
        print("\n\n" + "==="*30)
        print('Computing time taken...')
        print("==="*30)

        TimeDict = evalSummarizer.parseTime()
        timeDF = pd.DataFrame(TimeDict)
        timeDF["Mean Time"] = timeDF.mean(axis=1)
        timeDF["Std Time"] = timeDF.std(axis=1)
        timeDF.to_csv(outDir+'Times.csv')
    
    # Compute early precision
    if (opts.epr):
        print("\n" + "==="*30)
        print('Computing early precision values...')
        print("==="*30)
        ePRDF = evalSummarizer.computeEarlyPrec(undirected=False)

        ePRDF['Mean EP'] = ePRDF.mean(axis=1)
        ePRDF['Std EP'] = ePRDF.std(axis=1)
   
        ePRDF.to_csv(outDir + "EPr_directed.csv")

    # Compute early precision
    if (opts.epr_undirected):
        print("\n" + "==="*30)
        print('Computing early precision values...')
        print("==="*30)
        ePRDF = evalSummarizer.computeEarlyPrec(undirected=True)

        ePRDF['Mean EP'] = ePRDF.mean(axis=1)
        ePRDF['Std EP'] = ePRDF.std(axis=1)
   
        ePRDF.to_csv(outDir + "EPr_undirected.csv")
                        
    # Compute early precision for activation and inhibitory edges
    if (opts.sepr):
        print("\n\n" + "==="*30)
        print('Computing early precision values for activation and inhibitory edges...')
        print("==="*30)
        
        actDF, inhDF = evalSummarizer.computeSignedEPrec()
        actDF.to_csv(outDir + "EPr-Activation.csv")
        inhDF.to_csv(outDir + "EPr-Inhibitory.csv")

    # Compute median time taken
    if (opts.motifs):
        print("\n\n" + "==="*30)
        print('Computing network motifs...')
        print("==="*30)

        FBL, FFL, MI = evalSummarizer.computeNetMotifs()
        FBL.to_csv(outDir+'NetworkMotifs-FBL.csv')
        FFL.to_csv(outDir+'NetworkMotifs-FFL.csv')
        MI.to_csv(outDir+'NetworkMotifs-MI.csv')
        
    # Compute path statistics such as number of TP, FP, 
    # and path lengths among TP in the top-k networks.
    if (opts.paths):
        print('\n\nComputing path length statistics on predicted networks...')
        evalSummarizer.computePaths()
        
   # Compute edge ranked list using the borda method
    if (opts.borda):
        print('\n\nComputing edge ranked list using the borda method')
        evalSummarizer.computeBorda()


    print('\n\nEvaluation complete...\n')


if __name__ == '__main__':
  main()
