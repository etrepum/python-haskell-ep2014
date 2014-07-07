"""Breadth-first traversal"""



def breadth_first(starting_node,
                  edges):
    """Yield all nodes reachable from starting_node in breadth-first order"""
    visited = []
    queue = [starting_node]
    while queue:
        node = queue[0]; del queue[:1] # queue.pop(0)
        if node not in visited:
            yield node
            visited.append(node)
            queue.extend(edges[node])

GRAPH = {
    1: [1, 2, 3],
    2: [5],
    3: [4],
    4: [2],
    5: []
}

if __name__ == '__main__':
    print(list(breadth_first(1, GRAPH)))
