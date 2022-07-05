import pandas as pd
import numpy as np

def swap(genes):
    """
    Order Gene names.
    """
    if int(genes[0][1:]) < int(genes[1][1:]):
        return [genes[0],genes[1]]
    else:
        return [genes[1],genes[0]]

def make_undirected(dataset):
    """
    Make directed or partially directed edge list undirected by removing all duplicate edges and adding up corresponding edge weights.
    """
    # Order by genes
    dataset.loc[:,["Gene1","Gene2"]] = dataset.loc[:,["Gene1","Gene2"]].apply(swap,1,result_type='broadcast')

    # Get duplicate genes
    duplicates = dataset[dataset.duplicated(subset=["Gene1","Gene2"],keep=False)].sort_values(by=["Gene1", "Gene2"]).copy()

    # Return if no duplicates were found
    if (duplicates.empty == True):
        return dataset
    
    # Sum edge scores for duplicates
    duplicate_sums = duplicates.groupby(np.arange(len(duplicates))//2).mean()
    result = duplicates.iloc[1::2,:].copy().reset_index(drop=True)

    # Create final table
    result["EdgeWeight"] = duplicate_sums
    result = pd.concat([result, dataset.drop_duplicates(subset=["Gene1","Gene2"],keep=False)]).sort_values(by="EdgeWeight",ascending=False)

    return result

    
def swap_columns(df, col1, col2):
    """
    Define function to swap columns.
    """
    col_list = list(df.columns)
    x, y = col_list.index(col1), col_list.index(col2)
    col_list[y], col_list[x] = col_list[x], col_list[y]
    df = df[col_list]
    return df

def make_directed(dataset):
    """
    Make directed dataset from undirected dataset by duplicating all rows and halfing the edge weight.
    Only do this for undirected edge lists! Not for partially directed or directed edge lists.
    """
    temp = swap_columns(dataset, "Gene1", "Gene2")
    temp.columns = ["Gene1","Gene2","EdgeWeight"]
    result = pd.concat([dataset, temp], ignore_index=True).sort_values(by="EdgeWeight", ascending=False)
    #result.loc[:,["EdgeWeight"]] /= 2

    return result.reset_index(drop=True)