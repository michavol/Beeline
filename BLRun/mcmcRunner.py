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
    if not RunnerObj.inputDir.joinpath("MCMC").exists():
        print("Input folder for MCMC does not exist, creating input folder...")
        RunnerObj.inputDir.joinpath("MCMC").mkdir(exist_ok = False)
        
    if not RunnerObj.inputDir.joinpath("MCMC/ExpressionData.csv").exists():
          # input data
        ExpressionData = pd.read_csv(RunnerObj.inputDir.joinpath(RunnerObj.exprData),
                                     sep = '\t', header = 0)

        # Write .csv file
        ExpressionData.to_csv(RunnerObj.inputDir.joinpath("MCMC/ExpressionData.csv"),
                             sep = '\t', header = True, index = True)
    
def run(RunnerObj):
    '''
    Function to run MCMC algorithm
    '''
    inputPath = "data" + str(RunnerObj.inputDir).split(str(Path.cwd()))[1] + \
                    "/MCMC/ExpressionData.csv"
    
    # make output dirs if they do not exist:
    outDir = "outputs/"+str(RunnerObj.inputDir).split("inputs/")[1]+"/MCMC/"
    os.makedirs(outDir, exist_ok = True)
    
    outPath = "data/" +  str(outDir) + 'outFile.txt'
    cmdToRun = ' '.join(['docker run --rm -v', str(Path.cwd())+':/data/ 18881888/mcmc:base /bin/sh -c \"time -v -o', "data/" + str(outDir) + 'time.txt', 'Rscript runOrderMCMC.R',
                         inputPath, outPath, '\"'])
    print(cmdToRun)
    os.system(cmdToRun)



def parseOutput(RunnerObj):
    '''
    Function to parse outputs from MCMC.
    '''
   # Quit if output directory does not exist
    outDir = "outputs/"+str(RunnerObj.inputDir).split("inputs/")[1]+"/MCMC/"

        
    # Read output
    OutDF = pd.read_csv(outDir+'outFile.txt', sep = '\t', header = 0)
    
    if not Path(outDir+'outFile.txt').exists():
        print(outDir+'outFile.txt'+'does not exist, skipping...')
        return
    
    outFile = open(outDir + 'rankedEdges.csv','w')
    outFile.write('Gene1'+'\t'+'Gene2'+'\t'+'EdgeWeight'+'\n')

    for idx, row in OutDF.iterrows():
        outFile.write('\t'.join([row['Gene1'],row['Gene2'],str(row['EdgeWeight'])])+'\n')
    outFile.close()
    
