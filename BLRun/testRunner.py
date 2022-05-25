import os
import pandas as pd
from pathlib import Path
import numpy as np

def generateInputs(RunnerObj):
    '''
    Function to generate desired inputs for PPCOR.
    If the folder/files under RunnerObj.datadir exist, 
    this function will not do anything.
    '''
    if not RunnerObj.inputDir.joinpath("TEST").exists():
        print("Input folder for TEST does not exist, creating input folder...")
        RunnerObj.inputDir.joinpath("TEST").mkdir(exist_ok = False)
        
    if not RunnerObj.inputDir.joinpath("TEST/ExpressionData.csv").exists():
          # input data
        ExpressionData = pd.read_csv(RunnerObj.inputDir.joinpath(RunnerObj.exprData),
                                     sep = '\t', header = 0, index_col = 0)

        # Write .csv file
        ExpressionData.to_csv(RunnerObj.inputDir.joinpath("TEST/ExpressionData.csv"),
                             sep = '\t', header = True, index = False)
    
def run(RunnerObj):
    '''
    Function to run TEST algorithm
    '''
    inputPath = "data" + str(RunnerObj.inputDir).split(str(Path.cwd()))[1] + \
                    "/TEST/ExpressionData.csv"
    
    # make output dirs if they do not exist:
    outDir = "outputs/"+str(RunnerObj.inputDir).split("inputs/")[1]+"/TEST/"
    os.makedirs(outDir, exist_ok = True)
    
    outPath = "data/" +  str(outDir) + 'outFile.txt'
    cmdToRun = ' '.join(['docker run --rm -v', str(Path.cwd())+':/data/ 18881888/test:base /bin/sh -c \"time -v -o', "data/" + str(outDir) + 'time.txt', 'Rscript test.R',
                         inputPath, outPath, '\"'])
    print(cmdToRun)
    os.system(cmdToRun)



def parseOutput(RunnerObj):
    '''
    Function to parse outputs from TEST.
    '''
    # Quit if output directory does not exist
    outDir = "outputs/"+str(RunnerObj.inputDir).split("inputs/")[1]+"/TEST/"
    if not Path(outDir+'outFile.txt').exists():
        print(outDir+'outFile.txt'+'does not exist, skipping...')
        return
        
    # Read output
    OutDF = pd.read_csv(outDir+'outFile.txt', sep = '\t', header = 0)
    # edges with significant p-value

    OutDF.to_csv(outDir + 'rankedEdges.csv', header=False, index=False)
    # part1 = OutDF.loc[OutDF['pValue'] <= float(RunnerObj.params['pVal'])]
    # part1 = part1.assign(absCorVal = part1['corVal'].abs())
    # # edges without significant p-value
    # part2 = OutDF.loc[OutDF['pValue'] > float(RunnerObj.params['pVal'])]
    
    # outFile = open(outDir + 'rankedEdges.csv','w')
    # outFile.write('Gene1'+'\t'+'Gene2'+'\t'+'EdgeWeight'+'\n')

    # for idx, row in part1.sort_values('absCorVal', ascending = False).iterrows():
    #     outFile.write('\t'.join([str(row['Gene1']),str(row['Gene2']),str(row['corVal'])])+'\n')
    
    # for idx, row in part2.iterrows():
    #     outFile.write('\t'.join([str(row['Gene1']),str(row['Gene2']),str(0)])+'\n')
    # outFile.close()
    