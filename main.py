'''
Proszę założyć projekt na githubie, udostępnić go studentom z grupy oraz
zaimplementować produkcję (P1) i (P2) wraz z wizualizacją grafu wykorzystując
współrzędne wierzchołków i umożliwiając wybór poziomu grafu do wizualizacji.
Proszę napisać testy jednostkowe do produkcji (P1) i (P2) oraz do wizualizacji
grafu oraz umieścić produkcję oraz testy w githubie
'''


"""
attributes:
- label - El, E, I, i, (proposition: instead of using 'El' for the first elment we could use 'I')
- x, y - 1.0, 2.0
- level - 1, 2, ..
- children - optional, seems redundant.
- parent - optional, this could be speedup our computation a bit.
"""


"""
Let's start with generating P1.
"""


import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint as pp
from typing import Union, List, Tuple, Dict, Any, Optional

LEVEL_ATTRIBUTE = 'level'
LABEL_ATTRIBUTE = 'label'
X_ATTRIBUTE = 'x'
Y_ATTRIBUTE = 'label'


def draw(graph: nx.Graph) -> None:
    pos = nx.spring_layout(graph)
    pp(pos)
    
    # get axes
    ax = plt.gca()
    
    nx.draw(graph, pos, ax, with_labels=True)
    plt.savefig('test_draw.png')
    

def find_parents(graph: nx.Graph, level: int, label: str) -> list:
    parents = []
    for node in graph.nodes:
        if graph.nodes[node][LEVEL_ATTRIBUTE] == level - 1 and graph.nodes[node][LABEL_ATTRIBUTE] == label:
            parents.append(node)
    return parents

def node_comparator(found_node, searched_node) -> bool:
    # pp(f"Found node: {found_node}")
    # pp(f"Searched node: {searched_node}")
    # pp(f"Level: {found_node[LEVEL_ATTRIBUTE] == searched_node[LEVEL_ATTRIBUTE]}")
    # pp(f"Label: {found_node[LABEL_ATTRIBUTE] == searched_node[LABEL_ATTRIBUTE]}")
    # pp(f"Result: {found_node[LEVEL_ATTRIBUTE] == searched_node[LEVEL_ATTRIBUTE] and found_node[LABEL_ATTRIBUTE] == searched_node[LABEL_ATTRIBUTE]}")
    # pp("")
    return found_node[LEVEL_ATTRIBUTE] == searched_node[LEVEL_ATTRIBUTE] and found_node[LABEL_ATTRIBUTE] == searched_node[LABEL_ATTRIBUTE]

def find_isomporphic(graph: nx.Graph, left_side_graph: nx.Graph) -> list:
    # parents = find_parents(graph, 1, 'El')
    isomorphic_graphs = []
    # for parent in parents:
    for isomorphic_graph in nx.algorithms.isomorphism.GraphMatcher(graph, left_side_graph, node_match=node_comparator).subgraph_isomorphisms_iter():
        isomorphic_graphs.append(isomorphic_graph)
    return isomorphic_graphs

def p1():
    left_production_side_graph = nx.Graph()
    left_production_side_graph.add_nodes_from([
        (0, dict(label='El', x=1.0, y=1.0, level=0))
    ])

    right_production_side = nx.Graph()
    right_production_side.add_nodes_from([
        (0, dict(label='el', x=1.0, y=1.0, level=0)),
        (1, dict(label='I', x=2.0, y=1.0, level=0)),
        (2, dict(label='I', x=3.0, y=1.0, level=0)),
        (3, dict(label='E', x=4.0, y=1.0, level=0)),
        (4, dict(label='E', x=5.0, y=1.0, level=0)),
        (5, dict(label='E', x=5.0, y=1.0, level=0)),
        (6, dict(label='E', x=5.0, y=1.0, level=0))
    ])

    right_production_side.add_edges_from([
        (3,4), (3,6), (3,1), (4,5), (4,6), (4,1), (4,2), (5,2), (5,6), (6,1), (6,2), (0,1), (0,2),
    ])

    find_isomporphic(left_production_side_graph)
    pass

if __name__ == '__main__':
    initial_graph = nx.Graph()
    initial_graph.add_node(0, label='el', x=1.0, y=1.0, level=0)

    initial_graph.add_node(1, label='I', x=2.0, y=1.0, level=0)
    initial_graph.add_node(2, label='I', x=3.0, y=1.0, level=0)
    
    initial_graph.add_node(3, label='E', x=4.0, y=1.0, level=0)
    initial_graph.add_node(4, label='E', x=5.0, y=1.0, level=0)
    initial_graph.add_node(5, label='E', x=5.0, y=1.0, level=0)
    initial_graph.add_node(6, label='E', x=5.0, y=1.0, level=0)

    initial_graph.add_edge(3,4)
    initial_graph.add_edge(3,6)
    initial_graph.add_edge(3,1)
    initial_graph.add_edge(4,5)
    initial_graph.add_edge(4,6)
    initial_graph.add_edge(4,1)
    initial_graph.add_edge(4,2)
    initial_graph.add_edge(5,2)
    initial_graph.add_edge(5,6)
    initial_graph.add_edge(6,1)
    initial_graph.add_edge(6,2)
    initial_graph.add_edge(0,1)
    initial_graph.add_edge(0,2)
    
    test_graph = nx.Graph()
    test_graph.add_node(0, label='el', x=1.0, y=1.0, level=0)

    test_nodes = find_isomporphic(initial_graph, test_graph)

    print(f"Found {len(test_nodes)} isomorphic graphs.")
    print(f"Isomorphic graphs: {test_nodes}")

    # print('Gonna be fun!')