### Load libraries
library(pcalg)
suppressMessages(library(igraph))
library(reshape2)

### Parse Arguments
args <- commandArgs(trailingOnly = T)
inFile <- args[1]
outFile <- args[2]

nIter <- as.numeric(args[3])
partially_directed = as.numeric(args[4])
alpha = as.numeric(args[5])
verbose = as.numeric(args[6])
sample_size = as.numeric(args[7])

### Load data
df <- read.csv(inFile, header = TRUE, sep = "\t")

### Perform PC algorithm
dags_adj <- matrix(0, nrow=ncol(df), ncol=ncol(df))

### Set seed
set.seed(10023)

for (i in 1:nIter) {
  smp_size <- floor(sample_size * nrow(df))
  smp <- sample(seq_len(nrow(df)), size = smp_size)
  df_smp <- df[smp,]

  # Compute sufficient statistics
  suffStat <- list(C = cor(df_smp), n = nrow(df_smp))

  # Run pc algorithm
  pc.fit <- pc(suffStat=suffStat,
               indepTest = gaussCItest,
               alpha=alpha,
               labels=colnames(df_smp),
               verbose=verbose)
               #u2pd = "retry")
  
  if(partially_directed){
    # Generate edge weights for partially directed graph
    dag <- t(as(pc.fit, "matrix"))
    dags_adj = dags_adj + dag
    
  }else{
    # Generate edge weights for directed graph
    pdag <- udag2pdag(pc.fit)
    dag_nel <- pdag2dag(pdag@graph)
    dag <- graph_from_graphnel(dag_nel$graph)
    dags_adj = dags_adj + as_adj(dag)
  }
  
}

### Retrieve edge weights
dags_adj = dags_adj/nIter


### Convert to format that is expected by BEELINE framework
dags_edge_list <- melt(as.matrix(dags_adj))
dags_edge_list <- subset(dags_edge_list, Var1 != Var2)  #Remove self-cycles
dags_edge_list <- dags_edge_list[order(-dags_edge_list$value), ]#Order by edge weight


### Store as csv
colnames(dags_edge_list) = c("Gene1", "Gene2", "EdgeWeight")
write.table(dags_edge_list, file=outFile, sep = "\t", row.names = FALSE)