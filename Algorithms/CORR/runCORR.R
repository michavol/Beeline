### Load libraries
suppressMessages(library(psych))

### Parse Arguments
args <- commandArgs(trailingOnly = T)
inFile <- args[1]
outFile <- args[2]

### Read data
inputExpr <- read.table(inFile, sep="\t", header = 1)
geneNames <- colnames(inputExpr)

### Compute correlation and p-value matrix
corr <- cor(inputExpr, method = 'pearson')
#p.matrix <- corr.test(inputExpr, adjust = 'holm')$p

### Create output as for ppcor
DF = data.frame(Gene1 = geneNames[c(row(corr))], Gene2 = geneNames[c(col(corr))]
                , corVal = c(corr), pValue = c(corr)) #Fill pValue with correlations when not needed
outDF <- DF[order(DF$corVal, decreasing=TRUE), ]
outDF <- outDF[outDF$Gene1 != outDF$Gene2, ]

Nth.delete<-function(dataframe, n)dataframe[-(seq(n,to=nrow(dataframe),by=n)),]
outDF <- Nth.delete(outDF,2)

### Store results
write.table(outDF, outFile, sep = "\t", quote = FALSE, row.names = FALSE)
