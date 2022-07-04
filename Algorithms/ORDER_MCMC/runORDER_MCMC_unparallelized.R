### Load libraries
library(reshape2)
library(BiDAG)

### Parse Arguments
args <- commandArgs(trailingOnly = T)
inFile <- args[1]
outFile <- args[2]
nIter <- as.numeric(args[3])
sample_size <- as.numeric(args[4])

### Load data
df <- read.csv(inFile, header = TRUE, sep = "\t")
nrows <- NROW(df)

### Load library and initialize parameters
bge_score <- scoreparameters("bge", df)

### Set seed
set.seed(2022)

### Run orderMCMC
dags_adj <- matrix(0, nrow=ncol(df), ncol=ncol(df))

for (i in 1:nIter) {

    # Get sample size
    smp_size <- nrow(df)
    
    # Sample with replacement
    smp <- sample(seq_len(nrow(df)), size = smp_size, replace = T)
 
    # Retrieve DAG
    bge_score <- scoreparameters("bge", df[smp,])
    orderMAPfit <- orderMCMC(bge_score, 
                                    chainout = FALSE, 
                                    cpdag = TRUE)

    dags_adj <- dags_adj + orderMAPfit$DAG
}
# Average over DAG
dags_adj = dags_adj/nIter


### Convert to format that is expected by BEELINE framework
dags_edge_list <- melt(as.matrix(dags_adj))
dags_edge_list <- subset(dags_edge_list, Var1 != Var2)  #Remove self-cycles
dags_edge_list <- dags_edge_list[order(-dags_edge_list$value), ]#Order by edge weight


### Store as csv
colnames(dags_edge_list) = c("Gene1", "Gene2", "EdgeWeight")
write.table(dags_edge_list, file=outFile, sep = "\t", row.names = FALSE)