### Load libraries
library(reshape2)
library(BiDAG)
suppressMessages(library(foreach))
suppressMessages(library(doParallel))

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

### Run orderMCMC in parallel
#setup parallel backend to use many processors
cores=detectCores()
cl <- makeCluster(cores[1]-1) #not to overload your computer
registerDoParallel(cl)

dags_adj <- foreach(i=1:nIter, .combine='+') %dopar% {
    # Get sample size
    smp_size <- nrow(df)
    
    # Sample with replacement
    smp <- sample(seq_len(nrow(df)), size = smp_size, replace = T)
 
    # Retrieve DAG
    bge_score <- BiDAG::scoreparameters("bge", df[smp,])
    orderMAPfit <- BiDAG::orderMCMC(bge_score, 
                                    chainout = FALSE, 
                                    cpdag = TRUE)

    orderMAPfit$DAG
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