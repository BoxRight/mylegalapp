import torch
# Helper Functions
# ---------------------------

def create_co_occurrence_matrix(chains):
    """Creates a co-occurrence matrix from given chains."""
    max_term = max(max(chain) for chain in chains)  # get the maximum term to define matrix dimensions
    co_occurrence = torch.zeros((max_term, max_term))

    for chain in chains:
        for i in range(len(chain)-1):
            antecedent = chain[i]
            for j in range(i+1, len(chain)):
                consequent = chain[j]
                co_occurrence[antecedent-1, consequent-1] += 1

    return co_occurrence

def form_super_chains(co_occurrence, threshold=1):
    """Forms super chains based on the co-occurrence matrix."""
    # Using a basic threshold for now, you can refine this
    threshold = 1
    super_chains = []

    for i in range(co_occurrence.size(0)):
        chain = [i+1]
        for j in range(co_occurrence.size(1)):
            if co_occurrence[i, j] >= threshold:
                chain.append(j+1)
        if len(chain) > 1:
            super_chains.append(chain)

    return super_chains

def traverse(matrix, start, current_chain):
    # Recursive function to traverse adjacency matrix and generate chains
    chains = []
    next_nodes = torch.nonzero(matrix[current_chain[-1]])

    if len(next_nodes) == 0:
        return [current_chain]

    for node in next_nodes:
        node = node.item()
        if node not in current_chain:
            new_chain = current_chain + [node]
            chains.extend(traverse(matrix, start, new_chain))
        elif node == start:
            chains.append(current_chain)
    return chains

def numeric_tensor(chain):
    length = len(chain)
    tensor_rep = torch.zeros(length + 1, length).long()

    for i in range(length):
        tensor_rep[i, i:] = torch.tensor(chain[i:])

    return tensor_rep

def generate_binary_pattern(num_vars):
    binary_patterns = torch.ones(num_vars + 1, num_vars)
    for i in range(1, num_vars + 1):
        binary_patterns[i, :i] = 0
    return binary_patterns

def conditional_prob(tensor, given_value):
    """Calculate conditional probability of values in tensor given a specific value."""
    given_mask = tensor == given_value

    given_mask = tensor == given_value
    filtered_tensor = tensor[given_mask.any(dim=1)]
    values, counts = filtered_tensor.unique(return_counts=True)
    probabilities = (counts / filtered_tensor.size(0)).tolist()
    return dict(zip(values.tolist(), probabilities))

def filter_rows_by_selection(tensor, selection):
    """Filter tensor rows based on the user's selection."""
    """Function to filter tensor rows based on the user's selection."""
    return tensor[(tensor == selection).any(dim=1)]

def process_selected_numbers(selected_numbers, all_tensors, statement_dict):
    surviving_tensors = []
    for tensor in all_tensors:
        tensor_survives = True
        for selection in selected_numbers:
            filtered_tensor = filter_rows_by_selection(tensor, selection)
            if filtered_tensor.numel() == 0:
                tensor_survives = False
                break
        if tensor_survives:
            surviving_tensors.append(tensor)
    result_dict = {}
    for number in selected_numbers:
        for tensor in surviving_tensors:
            surviving_tensor_distribution = conditional_prob(tensor, number)
            for key in surviving_tensor_distribution.keys() & statement_dict.keys():
                prob = surviving_tensor_distribution[key]
                result_dict[statement_dict[key]] = prob
                
    requirements = []
    suggestions = []
    for i in result_dict:
        if not i:
            pass
        elif result_dict[i] == 1:
            requirements.append(i.title())
        elif result_dict[i] < 1 and result_dict[i] > 0:
            suggestions.append(f"It may be willfull that: {i.title()}")
            #fScore:{result_dict[i]}
    if not requirements and not suggestions:
        print("Returning error message")
        return {
            'error': f"The selected statements: {', '.join([statement_dict[num] for num in selected_numbers])} cannot be put together.".title()
        }
    return {'requirements': requirements, 'suggestions': suggestions}

