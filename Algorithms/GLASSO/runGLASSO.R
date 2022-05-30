### Load libraries
suppressMessages(library(igraph))
suppressMessages(library(glasso))

### Parse Arguments
args <- commandArgs(trailingOnly = T)
inFile <- args[1]
outFile <- args[2]
rho1 <- as.numeric(args[3])
rho2 <- as.numeric(args[4])
nIter <- as.numeric(args[5])
sample_size <- as.numeric(args[6])

### Load data
df <- read.csv(inFile, header = TRUE, sep = "\t")

### Set seed
set.seed(2022)


### Train graphical lasso (with bootstrapping for edge confidence)
# https://cran.r-project.org/web/packages/glasso/glasso.pdf
precision.matrix.boots <- matrix(0, nrow=ncol(df), ncol=ncol(df))

for (i in 1:nIter) {
  smp_size <- floor(sample_size * nrow(df))
  smp_ind <- sample(seq_len(nrow(df)), size = smp_size)
  smp <- df[smp_ind,]
  
  variance.matrix <- var(smp)
  glasso.result <- glasso(variance.matrix, rho=rho1)
  glasso.result.precond <- glasso(variance.matrix, rho=rho2, w.init=glasso.result$w, wi.init=glasso.result$wi, start='warm')
  precision.matrix <- glasso.result.precond$wi
 
  precision.matrix.boots = precision.matrix.boots + precision.matrix
}

# Normalize over bootstraps
precision.matrix.boots = precision.matrix.boots/nIter

# Remove self-cycles and represent undirected with only one edge per pair
precision.matrix.boots[lower.tri(precision.matrix.boots, diag=TRUE)] <- 0
  
# Remove self-cycles and represent undirected with only one edge per pair
precision.matrix.boots[lower.tri(precision.matrix.boots, diag=TRUE)] <- 0

# Update gene names
rownames(precision.matrix.boots) <- colnames(precision.matrix.boots) <- colnames(df)

# Extract edge list from results
uag_edge_list <- graph.adjacency(precision.matrix.boots, weighted=TRUE)
uag_edge_list <- get.data.frame(uag_edge_list)
colnames(uag_edge_list) <- c("Gene1", "Gene2", "EdgeWeight")


### Prepare format for Beeline
# Order by edge weight
uag_edge_list <- uag_edge_list[order(-abs(uag_edge_list$EdgeWeight)), ]

### Save results
write.table(uag_edge_list, file=outFile, sep = "\t", row.names = FALSE)
