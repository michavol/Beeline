# Include packages

using NetworkInference
using LightGraphs

algorithm = PIDCNetworkInference()

dataset_name = string(ARGS[1])

@time genes = get_nodes(dataset_name);
print(dataset_name)
@time network = InferredNetwork(algorithm, genes);
# print(genes)
# print(network)
write_network_file(string(ARGS[2]), network);

