### Load libraries
suppressMessages(library(igraph))
suppressMessages(library(glasso))
suppressMessages(library(foreach))
suppressMessages(library(doParallel))

### Parse Arguments
args <- commandArgs(trailingOnly = T)
inFile <- args[1]
outFile <- args[2]
rho1 <- as.numeric(args[3])
rho2 <- as.numeric(args[4])

### Load data
df <- read.csv(inFile, header = TRUE, sep = "\t")

### Set seed
set.seed(2022)

### Apply glasso
variance.matrix <- var(df)
glasso.result <- glasso::glasso(variance.matrix, 
                                rho=rho1)
glasso.result.precond <- glasso::glasso(variance.matrix, 
                                        rho=rho2, 
                                        w.init=glasso.result$w, 
                                        wi.init=glasso.result$wi, start='warm')
precision.matrix <- glasso.result.precond$wi

### Create undirected graph
# Remove self-cycles and represent undirected with only one edge per pair
precision.matrix[lower.tri(precision.matrix, diag=TRUE)] <- 0

# Update gene names
rownames(precision.matrix) <- colnames(precision.matrix) <- colnames(df)

# Extract edge list from results
uag_edge_list <- graph.adjacency(precision.matrix, weighted=TRUE)
uag_edge_list <- get.data.frame(uag_edge_list)
colnames(uag_edge_list) <- c("Gene1", "Gene2", "EdgeWeight")


### Prepare format for Beeline
# Order by edge weight
uag_edge_list <- uag_edge_list[order(-abs(uag_edge_list$EdgeWeight)), ]

### Save results
write.table(uag_edge_list, file=outFile, sep = "\t", row.names = FALSE)