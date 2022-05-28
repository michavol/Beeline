### Load libraries
library(reshape2)
library(BiDAG)

### Parse Arguments
args <- commandArgs(trailingOnly = T)
inFile <- args[1]
outFile <- args[2]
nIter <- as.numeric(args[3])

### Load data
df <- read.csv(inFile, header = TRUE, sep = "\t")
nrows <- NROW(df)

if (nrows == 1)
{
  df <- df[rep(seq_len(nrow(df)), each = 3), ]
}

### Load library and initialize parameters
bge_score <- scoreparameters("bge", df)

### Learn Bayesian network using MCMC and get edge weights by bootstrapping
set.seed(2022)
dags_adj <- matrix(0, nrow=ncol(df), ncol=ncol(df))
#nIter = 10

for (i in 1:nIter) {
  if (nrows == 1)
  {
    bge_score <- scoreparameters("bge", df)
  }
  else
  {
    smp_size <- floor(0.8 * nrow(df))
    smp <- sample(seq_len(nrow(df)), size = smp_size)
 
    bge_score <- scoreparameters("bge", df[smp,])
  }
  
  orderMAPfit <- orderMCMC(bge_score)
  dags_adj = dags_adj + orderMAPfit$DAG
}

dags_adj = dags_adj/nIter


### Convert to format that is expected by BEELINE framework
dags_edge_list <- melt(as.matrix(dags_adj))
dags_edge_list <- subset(dags_edge_list, Var1 != Var2)  #Remove self-cycles
dags_edge_list <- dags_edge_list[order(-dags_edge_list$value), ]#Order by edge weight


### Store as csv
colnames(dags_edge_list) = c("Gene1", "Gene2", "EdgeWeight")
write.table(dags_edge_list, file=outFile, sep = "\t", row.names = FALSE)