### Load libraries
suppressMessages(library(GENIE3))

### Parse Arguments
args <- commandArgs(trailingOnly = T)
inFile <- args[1]
outFile <- args[2]
nTrees <- as.numeric(args[3])
nCores <- as.numeric(args[4])
treeMethod <- args[5]
K <- args[6]

### Read data
inputExpr <- t(read.table(inFile, sep="\t", header = 1))

### Run GENIE3
set.seed(123)
weightMatrix <- GENIE3(inputExpr, 
                       treeMethod = treeMethod,
                       K = K,
                       nTrees = nTrees,
                       nCores = nCores)
linkList <- getLinkList(weightMatrix)
colnames(linkList) <- c("Gene1","Gene2","EdgeWeight")

### Store results
write.table(linkList, file=outFile, sep = "\t", row.names = FALSE)
