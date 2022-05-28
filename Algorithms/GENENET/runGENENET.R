### Load libraries
suppressMessages(library(GeneNet))
suppressMessages(library(graph))

### Parse Arguments
args <- commandArgs(trailingOnly = T)
inFile <- args[1]
outFile <- args[2]
num_edges = as.numeric(args[3])
directed = as.numeric(args[4])
verbose = as.numeric(args[5])

# Load data
df <- read.csv(inFile, header = TRUE, sep = "\t")

# Infer Model
pcor.dyn = ggm.estimate.pcor(as.matrix(df), method = "dynamic", verbose = verbose)
arth.edges = network.test.edges(pcor.dyn,direct=directed, verbose = verbose)
#dim(arth.edges)

# We use the strongest edges:
arth.net = extract.network(arth.edges, method.ggm="number", cutoff.ggm=num_edges, verbose=verbose)

# Construct Graph
node.labels = colnames(df)
gr = network.make.graph(arth.net, node.labels, drop.singles=TRUE) 

# Set edge attributes:
edi = edge.info(gr) # edge directions and correlations
edge_weights <- as.matrix(edi$weight)


# Convert rownames into columns containing gene names of edges
edges <- rownames(edge_weights)
split <- function(edge_str)
{
  return (strsplit(edge_str, "~", fixed=TRUE))
}
edges <- mapply(split,edges)

gene1 <- c()
gene2 <- c()

for (i in 1:length(edges)) {
  gene1 <- c(gene1, edges[[i]][1])
  gene2 <- c(gene2, edges[[i]][2])
}

# Construct dataframe and sort by decreasing absolute weight
dags_edge_list <- data.frame(Gene1=gene1, Gene2=gene2, EdgeWeight=edge_weights)
dags_edge_list <- dags_edge_list[order(-abs(dags_edge_list$EdgeWeight)), ]#Order by edge weight

# Store results
write.table(dags_edge_list, file=outFile, sep = "\t", row.names = FALSE)