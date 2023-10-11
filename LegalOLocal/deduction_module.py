from data_processing import (
    create_co_occurrence_matrix, 
    form_super_chains, 
    traverse, 
    numeric_tensor, 
    generate_binary_pattern,
    conditional_prob,
    filter_rows_by_selection,
    torch
)
from database import rows

# Main Processing
# ---------------------------

def main():
    """Main function to process data and generate tensor representations of super chains."""

    # Initialization: Create an empty adjacency matrix
    max_value = max(max(row) for row in rows)
    adj_matrix = torch.zeros((max_value, max_value))

    # Populate the adjacency matrix based on the rows
    for row in rows:
        adj_matrix[row[0]-1, row[1]-1] = 1

    # Generate chains starting from each point in the matrix
    result_chains = []
    for i in range(max_value):
        chains_from_i = traverse(adj_matrix, i, [i])
        result_chains.extend(chains_from_i)

    # Adjust index of the chains to start from 1
    result_chains = [[i+1 for i in chain] for chain in result_chains]

    # Create the co-occurrence matrix and derive super chains
    co_occurrence = create_co_occurrence_matrix(result_chains)

    super_chains = form_super_chains(co_occurrence)

    # Derive chains from the adjacency matrix
    chains = [torch.nonzero(adj_matrix[i]).squeeze().tolist() for i in range(adj_matrix.size(0))]
    chains = [chain for chain in chains if chain]

    # Convert each super chain into tensor representations
    all_tensors = []
    for chain in super_chains:
        variables = torch.tensor(chain)
        num_vars = len(variables)
        binary_patterns = generate_binary_pattern(num_vars)
        numeric_tensors = numeric_tensor(chain)
        all_tensors.append(numeric_tensors)

    return all_tensors
