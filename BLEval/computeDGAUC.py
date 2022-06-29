import pandas as pd
import numpy as np
import seaborn as sns
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(rc={"lines.linewidth": 2}, palette  = "deep", style = "ticks")
from sklearn.metrics import precision_recall_curve, roc_curve, auc
from itertools import product, permutations, combinations, combinations_with_replacement
from tqdm import tqdm
from rpy2.robjects.packages import importr
from rpy2.robjects import FloatVector


def PRROC(dataDict, inputSettings, directed = True, selfEdges = False, plotFlag = False):
    '''
    Computes areas under the precision-recall and ROC curves
    for a given dataset for each algorithm.
    

    :param directed:   A flag to indicate whether to treat predictions as directed edges (directed = True) or undirected edges (directed = False).
    :type directed: bool
    :param selfEdges:   A flag to indicate whether to includeself-edges (selfEdges = True) or exclude self-edges (selfEdges = False) from evaluation.
    :type selfEdges: bool
    :param plotFlag:   A flag to indicate whether or not to save PR and ROC plots.
    :type plotFlag: bool
        
    :returns:
            - AUPRC: A dictionary containing AUPRC values for each algorithm
            - AUROC: A dictionary containing AUROC values for each algorithm
    '''
    
    # Read file for trueEdges
    # trueEdgesDF = pd.read_csv(str(inputSettings.datadir)+'/'+ dataDict['name'] +
    #                             '/' +dataDict['trueEdges'],
    #                             sep = ',', 
    #                             header = 0)#, index_col = None)

    headerList = ['Gene1', 'Gene2', 'Type']
    
    trueEdgesDF = pd.read_csv(str(inputSettings.datadir)+'/'+ dataDict['name'] +
                                '/' +dataDict['trueEdges'],
                                sep = '\t', 
                                header = 0, index_col = None)
    
    trueEdgesDF.columns = headerList

    trueEdgesDF = trueEdgesDF[trueEdgesDF["Type"] != 0]

    # Initialize data dictionaries

    precisionDict = {}
    recallDict = {}
    FPRDict = {}
    TPRDict = {}
    AUPRC = {}
    AUROC = {}

    # set-up outDir that stores output directory name
    outDir = "outputs/"+str(inputSettings.datadir).split("inputs/")[1]+ '/' +dataDict['name']
    
    if directed:
        for algo in tqdm(inputSettings.algorithms, 
                        total = len(inputSettings.algorithms), unit = " Algorithms"):

        # for algo in inputSettings.algorithms:

            # check if the output rankedEdges file exists
            if Path(outDir + '/' +algo[0]+'/rankedEdges.csv').exists():
                 # Initialize Precsion

                predDF = pd.read_csv(outDir + '/' +algo[0]+'/rankedEdges.csv', \
                                            sep = '\t', header =  0, index_col = None)

                if (algo[0] in ["GLASSO", "PPCOR", "GENENET", "ARACNE", "CORR"]):
                    predDF = make_directed(predDF)

                precisionDict[algo[0]], recallDict[algo[0]], FPRDict[algo[0]], TPRDict[algo[0]], AUPRC[algo[0]], AUROC[algo[0]] = computeScores(trueEdgesDF, predDF, directed = True, selfEdges = selfEdges)

            else:
                print(outDir + '/' +algo[0]+'/rankedEdges.csv', \
                      ' does not exist. Skipping...')
            PRName = '/PRplot'
            ROCName = '/ROCplot'
    else:
        for algo in tqdm(inputSettings.algorithms, 
                         total = len(inputSettings.algorithms), unit = " Algorithms"):

        # for algo in inputSettings.algorithms:
                       
            # check if the output rankedEdges file exists
            if Path(outDir + '/' +algo[0]+'/rankedEdges.csv').exists():
                 # Initialize Precision

                predDF = pd.read_csv(outDir + '/' +algo[0]+'/rankedEdges.csv', \
                                            sep = '\t', header =  0, index_col = None)

                # Convert edge list to undirected edge list if directed == False
                predDF = make_undirected(predDF)


                precisionDict[algo[0]], recallDict[algo[0]], FPRDict[algo[0]], TPRDict[algo[0]], AUPRC[algo[0]], AUROC[algo[0]] = computeScores(trueEdgesDF, predDF, directed = False, selfEdges = selfEdges)

            else:
                print(outDir + '/' +algo[0]+'/rankedEdges.csv', \
                  ' does not exist. Skipping...')
            
            PRName = '/uPRplot'
            ROCName = '/uROCplot'
    if (plotFlag):
         ## Make PR curves
        legendList = []
        for key in recallDict.keys():
            sns.lineplot(recallDict[key],precisionDict[key], ci=None)
            legendList.append(key + ' (AUPRC = ' + str("%.2f" % (AUPRC[key]))+')')
        plt.xlim(0,1)    
        plt.ylim(0,1)
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.legend(legendList) 
        plt.savefig(outDir+PRName+'.pdf')
        plt.savefig(outDir+PRName+'.png')
        plt.clf()

        ## Make ROC curves
        legendList = []
        for key in recallDict.keys():
            sns.lineplot(FPRDict[key],TPRDict[key], ci=None)
            legendList.append(key + ' (AUROC = ' + str("%.2f" % (AUROC[key]))+')')

        plt.plot([0, 1], [0, 1], linewidth = 1.5, color = 'k', linestyle = '--')

        plt.xlim(0,1)    
        plt.ylim(0,1)
        plt.xlabel('FPR')
        plt.ylabel('TPR')
        plt.legend(legendList) 
        plt.savefig(outDir+ROCName+'.pdf')
        plt.savefig(outDir+ROCName+'.png')
        plt.clf()
    return AUPRC, AUROC

def computeScores(trueEdgesDF, predEdgeDF, 
                  directed = True, selfEdges = True):
    '''        
    Computes precision-recall and ROC curves
    using scikit-learn for a given set of predictions in the 
    form of a DataFrame.
    
    :param trueEdgesDF:   A pandas dataframe containing the true classes.The indices of this dataframe are all possible edgesin a graph formed using the genes in the given dataset. This dataframe only has one column to indicate the classlabel of an edge. If an edge is present in the reference network, it gets a class label of 1, else 0.
    :type trueEdgesDF: DataFrame
        
    :param predEdgeDF:   A pandas dataframe containing the edge ranks from the prediced network. The indices of this dataframe are all possible edges.This dataframe only has one column to indicate the edge weightsin the predicted network. Higher the weight, higher the edge confidence.
    :type predEdgeDF: DataFrame
    
    :param directed:   A flag to indicate whether to treat predictionsas directed edges (directed = True) or undirected edges (directed = False).
    :type directed: bool
        
    :param selfEdges:   A flag to indicate whether to includeself-edges (selfEdges = True) or exclude self-edges (selfEdges = False) from evaluation.
    :type selfEdges: bool
        
    :returns:
            - prec: A list of precision values (for PR plot)
            - recall: A list of precision values (for PR plot)
            - fpr: A list of false positive rates (for ROC plot)
            - tpr: A list of true positive rates (for ROC plot)
            - AUPRC: Area under the precision-recall curve
            - AUROC: Area under the ROC curve
    '''

    if directed:        
        # Initialize dictionaries with all 
        # possible edges
        if selfEdges:
            possibleEdges = list(product(np.unique(trueEdgesDF.loc[:,['Gene1','Gene2']]),
                                         repeat = 2))
        else:
            possibleEdges = list(permutations(np.unique(trueEdgesDF.loc[:,['Gene1','Gene2']]),
                                         r = 2))
        
        TrueEdgeDict = {'|'.join(p):0 for p in possibleEdges}
        PredEdgeDict = {'|'.join(p):0 for p in possibleEdges}
        
        # Compute TrueEdgeDict Dictionary
        # 1 if edge is present in the ground-truth
        # 0 if edge is not present in the ground-truth
        for key in TrueEdgeDict.keys():
            if len(trueEdgesDF.loc[(trueEdgesDF['Gene1'] == key.split('|')[0]) &
                   (trueEdgesDF['Gene2'] == key.split('|')[1])])>0:
                    TrueEdgeDict[key] = 1
                
        for key in PredEdgeDict.keys():
            subDF = predEdgeDF.loc[(predEdgeDF['Gene1'] == key.split('|')[0]) &
                               (predEdgeDF['Gene2'] == key.split('|')[1])]
            if len(subDF)>0:
                PredEdgeDict[key] = np.abs(subDF.EdgeWeight.values[0])

    # if undirected
    else:
        
        # Initialize dictionaries with all 
        # possible edges
        if selfEdges:
            possibleEdges = list(combinations_with_replacement(np.unique(trueEdgesDF.loc[:,['Gene1','Gene2']]),
                                                               r = 2))
        else:
            possibleEdges = list(combinations(np.unique(trueEdgesDF.loc[:,['Gene1','Gene2']]),
                                                               r = 2))
        TrueEdgeDict = {'|'.join(p):0 for p in possibleEdges}
        PredEdgeDict = {'|'.join(p):0 for p in possibleEdges}

        # Compute TrueEdgeDict Dictionary
        # 1 if edge is present in the ground-truth
        # 0 if edge is not present in the ground-truth

        for key in TrueEdgeDict.keys():
            if len(trueEdgesDF.loc[((trueEdgesDF['Gene1'] == key.split('|')[0]) &
                           (trueEdgesDF['Gene2'] == key.split('|')[1])) |
                              ((trueEdgesDF['Gene2'] == key.split('|')[0]) &
                           (trueEdgesDF['Gene1'] == key.split('|')[1]))]) > 0:
                TrueEdgeDict[key] = 1  

        # Compute PredEdgeDict Dictionary
        # from predEdgeDF

        for key in PredEdgeDict.keys():
            subDF = predEdgeDF.loc[((predEdgeDF['Gene1'] == key.split('|')[0]) &
                               (predEdgeDF['Gene2'] == key.split('|')[1])) |
                              ((predEdgeDF['Gene2'] == key.split('|')[0]) &
                               (predEdgeDF['Gene1'] == key.split('|')[1]))]
            if len(subDF)>0:
                PredEdgeDict[key] = max(np.abs(subDF.EdgeWeight.values))
    
                
    # Combine into one dataframe
    # to pass it to sklearn
    outDF = pd.DataFrame([TrueEdgeDict,PredEdgeDict]).T
    outDF.columns = ['TrueEdges','PredEdges']
    prroc = importr('PRROC')
    prCurve = prroc.pr_curve(scores_class0 = FloatVector(list(outDF['PredEdges'].values)), 
              weights_class0 = FloatVector(list(outDF['TrueEdges'].values)))

    fpr, tpr, thresholds = roc_curve(y_true=outDF['TrueEdges'],
                                     y_score=outDF['PredEdges'], pos_label=1)

    prec, recall, thresholds = precision_recall_curve(y_true=outDF['TrueEdges'],
                                                      probas_pred=outDF['PredEdges'], pos_label=1)
    
    return prec, recall, fpr, tpr, prCurve[2][0], auc(fpr, tpr)


def swap(genes):
    """
    Order Gene names.
    """
    if int(genes[0][1:]) < int(genes[1][1:]):
        return [genes[0],genes[1]]
    else:
        return [genes[1],genes[0]]

def make_undirected(dataset):
    """
    Make directed or partially directed edge list undirected by removing all duplicate edges and adding up corresponding edge weights.
    """
    # Order by genes
    dataset.loc[:,["Gene1","Gene2"]] = dataset.loc[:,["Gene1","Gene2"]].apply(swap,1,result_type='broadcast')

    # Get duplicate genes
    duplicates = dataset[dataset.duplicated(subset=["Gene1","Gene2"],keep=False)].sort_values(by=["Gene1", "Gene2"]).copy()

    # Return if no duplicates were found
    if (duplicates.empty == True):
        return dataset
    
    # Sum edge scores for duplicates
    duplicate_sums = duplicates.groupby(np.arange(len(duplicates))//2).sum()
    result = duplicates.iloc[1::2,:].copy().reset_index(drop=True)

    # Create final table
    result["EdgeWeight"] = duplicate_sums
    result = pd.concat([result, dataset.drop_duplicates(subset=["Gene1","Gene2"],keep=False)]).sort_values(by="EdgeWeight",ascending=False)

    return result

    
def swap_columns(df, col1, col2):
    """
    Define function to swap columns.
    """
    col_list = list(df.columns)
    x, y = col_list.index(col1), col_list.index(col2)
    col_list[y], col_list[x] = col_list[x], col_list[y]
    df = df[col_list]
    return df

def make_directed(dataset):
    """
    Make directed dataset from undirected dataset by duplicating all rows and halfing the edge weight.
    Only do this for undirected edge lists! Not for partially directed or directed edge lists.
    """
    temp = swap_columns(dataset, "Gene1", "Gene2")
    temp.columns = ["Gene1","Gene2","EdgeWeight"]
    result = pd.concat([dataset, temp], ignore_index=True).sort_values(by="EdgeWeight", ascending=False)
    result.loc[:,["EdgeWeight"]] /= 2

    return result.reset_index(drop=True)