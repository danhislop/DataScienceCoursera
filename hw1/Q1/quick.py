from submission import Graph, TMDBAPIUtils

def setUp(with_nodes_file=None, with_edges_file=None):
    graph = Graph(with_nodes_file, with_edges_file)
    return graph

if __name__ == "__main__":
    graph = Graph(with_nodes_file='nodes.csv', with_edges_file='edges.csv')
    print(graph.max_degree_nodes())
    print(graph.find_non_leaf_node_count())
    print(graph.find_lowest_degree())
    print("lowest count", len(graph.find_lowest_degree()))



