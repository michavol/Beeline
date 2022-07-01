### Load libraries
library(minet)
suppressMessages(library(igraph))

### Parse Arguments
args <- commandArgs(trailingOnly = T)
inFile <- args[1]
outFile <- args[2]
eps <- as.numeric(args[3])

### Load data
df <- read.csv(inFile, header = TRUE, sep = "\t")

### Set seed
set.seed(2022)

### Build a mutual information matrix
mutual.information <- build.mim(df, estimator = "spearman", disc = "none", nbins = sqrt(NROW(df)))

### Perform the Aracne Algorithm
net <- aracne(mutual.information, eps=eps)

### Prepare for Beeline
# Extract edge list from results
uag_edge_list <- graph.adjacency(net, weighted=TRUE)
uag_edge_list <- get.data.frame(uag_edge_list)
colnames(uag_edge_list) <- c("Gene1", "Gene2", "EdgeWeight")

# Prepare format for Beeline
# Remove self-cycles
uag_edge_list <- subset(uag_edge_list, Gene1 != Gene2)  
# Order by edge weight
uag_edge_list <- uag_edge_list[order(-abs(uag_edge_list$EdgeWeight)), ]

# Store as undirected graph
# Nth.delete<-function(dataframe, n)dataframe[-(seq(n,to=nrow(dataframe),by=n)),]
# uag_edge_list <- Nth.delete(uag_edge_list,2)

# Save results
write.table(uag_edge_list, file=outFile, sep = "\t", row.names = FALSE)
