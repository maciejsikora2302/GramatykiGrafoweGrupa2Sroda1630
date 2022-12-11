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
from copy import copy

class Attribute:
    LEVEL = 'level'
    LABEL = 'label'
    X = 'x'
    Y = 'y'


def draw(graph: nx.Graph, level: int = None, filename: str='test_draw.png') -> None:
    if level is not None:
        graph = graph.subgraph([node for node in graph.nodes if graph.nodes[node][Attribute.LEVEL] == level])
    
    pos = nx.spring_layout(graph)

    pos_labels = copy(pos)
    for node in graph.nodes():
        pos_labels[node] = (pos[node][0], pos[node][1] + 0.3)

    label_attr = nx.get_node_attributes(graph, Attribute.LABEL)
    xs = nx.get_node_attributes(graph, Attribute.X)
    ys = nx.get_node_attributes(graph, Attribute.Y)

    red_labels = ['El', 'el']
    blue_labels = ['E', 'e']
    yellow_labels = ['I', 'i']

    node_colors = []
    for node in graph.nodes():
        if label_attr[node] in red_labels:
            node_colors.append('red')
        elif label_attr[node] in blue_labels:
            node_colors.append('blue')
        elif label_attr[node] in yellow_labels:
            node_colors.append('yellow')
        else:
            node_colors.append('white')


    labels = { node: f'{label_attr[node], (xs[node], ys[node])}' for node in graph.nodes()}

    nx.draw_networkx_nodes(graph, pos, node_size=2000, node_color=node_colors, edgecolors='black', linewidths=5, alpha=0.5)
    nx.draw_networkx_edges(graph, pos, width=5, alpha=0.3)
    nx.draw_networkx_labels(graph, pos_labels, labels)

    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")
    plt.savefig(filename)
    plt.cla()
    plt.clf()
    

def find_parents(graph: nx.Graph, level: int, label: str) -> list:
    parents = []
    for node in graph.nodes:
        if graph.nodes[node][Attribute.LEVEL] == level - 1 and graph.nodes[node][Attribute.LABEL] == label:
            parents.append(node)
    return parents

def node_comparator(found_node, searched_node) -> bool:
    return found_node[Attribute.LABEL] == searched_node[Attribute.LABEL]
    # return found_node[Attribute.LEVEL] == searched_node[Attribute.LEVEL] and found_node[Attribute.LABEL] == searched_node[Attribute.LABEL]


def find_isomporphic(graph: nx.Graph, left_side_graph: nx.Graph) -> dict:
    # for isomorphic_graph in nx.algorithms.isomorphism.GraphMatcher(graph, left_side_graph, node_match=node_comparator).subgraph_isomorphisms_iter():
    #     return isomorphic_graph
    # return None
    isomorphic_graphs = []
    for isomorphic_graph in nx.algorithms.isomorphism.GraphMatcher(graph, left_side_graph, node_match=node_comparator).subgraph_isomorphisms_iter():
        isomorphic_graphs.append(isomorphic_graph)
    return isomorphic_graphs

def find_isomporphic_wrapper(graph: nx.Graph, left_side_graph: nx.Graph) -> dict:
    return find_isomporphic(graph, left_side_graph)

def p1(graph: nx.Graph):
    left_production_side_graph = nx.Graph()
    parent_tmp_node_number = 8

    left_production_side_graph.add_nodes_from([
        (parent_tmp_node_number, dict(label='El', x=1.0, y=1.0, level=0))
    ])
    pp(f"Initial left graph: {type(left_production_side_graph)}")

    n = len(graph.nodes)

    right_side_parent_node = (parent_tmp_node_number, dict(label='el', x=1.0, y=1.0, level=0)) # only new node is here!
    right_side_nodes_new = [
        (1, dict(label='I', x=2.0, y=1.0, level=1)), # others have to be generated!
        (2, dict(label='I', x=3.0, y=1.0, level=1)),
        (3, dict(label='E', x=4.0, y=1.0, level=1)),
        (4, dict(label='E', x=5.0, y=1.0, level=1)),
        (5, dict(label='E', x=5.0, y=1.0, level=1)),
        (6, dict(label='E', x=5.0, y=1.0, level=1))
    ]

    right_side_nodes = [right_side_parent_node] + right_side_nodes_new

    right_side_edges = [
        (3,4), (3,6), (3,1), (4,5), (4,6), (4,1), (4,2), (5,2), (5,6), (6,1), (6,2), (parent_tmp_node_number,1), (parent_tmp_node_number,2),
    ]

    right_production_side = nx.Graph()
    right_production_side.add_nodes_from(right_side_nodes)
    right_production_side.add_edges_from(right_side_edges)

    isomorphic_mapping = find_isomporphic_wrapper(graph, left_production_side_graph)[0]

    # create reverse mapping
    isomorphic_mapping_reverse = {v: k for k, v in isomorphic_mapping.items()}

    pp(f"Isomorphic mapping: {isomorphic_mapping}")
    pp(f"Isomorphic mapping reverse: {isomorphic_mapping_reverse}")

    # right_side_existing_node_mapped = isomorphic_mapping[right_side_nodes_existing[0]]

    right_side_nodes_mapping = { node[0]: node[0]+n for node in right_side_nodes_new } # define a dictionay mapping old node number (based on right_side_nodes ) => graph node.
    right_side_nodes_mapping[parent_tmp_node_number] = isomorphic_mapping_reverse[parent_tmp_node_number]
        

    right_side_edges_mapped = list(
        map(lambda edge: (right_side_nodes_mapping[edge[0]], right_side_nodes_mapping[edge[1]]), right_side_edges))

    right_side_nodes_mapped = list(
        map(lambda node: (right_side_nodes_mapping[node[0]], node[1]), right_side_nodes_new))
    
    existing_node_parent = graph.nodes[isomorphic_mapping_reverse[parent_tmp_node_number]]

    #increase level of all nodes in right_side_nodes_mapped
    for node in right_side_nodes_mapped:
        node[1][Attribute.LEVEL] = existing_node_parent[Attribute.LEVEL] + 1

    graph.nodes[isomorphic_mapping_reverse[parent_tmp_node_number]][Attribute.LABEL] = right_side_parent_node[1][Attribute.LABEL]


    graph.add_nodes_from(right_side_nodes_mapped)
    graph.add_edges_from(right_side_edges_mapped)

    # pp(f"Isomorphic graph: {type(isomorphic_graph)}")
    pp(f"Isomorphic graph size: {len(graph)}")
    pp(f"Isomorphic graph: {graph}")

    # print all labels
    for node in graph.nodes:
        print(graph.nodes[node][Attribute.LABEL])


def p2(graph: nx.Graph) -> None:
    left_production_side_graph = nx.Graph()

    parent_tmp_node_number = 8
    left_production_side_graph.add_nodes_from([
        (parent_tmp_node_number, dict(label='I', x=None, y=None, level=None))
        (1, dict(label='E', x=None, y=None, level=None)),
        (2, dict(label='E', x=None, y=None, level=None)),
        (3, dict(label='E', x=None, y=None, level=None)),
    ])
    left_production_side_graph.add_edges_from([
        (parent_tmp_node_number, 1),
        (parent_tmp_node_number, 2),
        (parent_tmp_node_number, 3),
        (1, 2),
        (1, 3),
        (2, 3)
    ])

    pp(f"Initial left graph: {left_production_side_graph}")

    draw(left_production_side_graph, 'left_production_side_graph.png')
    # n = len(graph.nodes)

    # right_side_parent_node = (parent_tmp_node_number, dict(label='el', x=1.0, y=1.0, level=0)) # only new node is here!
    # right_side_nodes_new = [
    #     (1, dict(label='I', x=None, y=None, level=None)), # others have to be generated!
    #     (2, dict(label='I', x=None, y=None, level=None)),
    #     (3, dict(label='E', x=None, y=None, level=None)),
    #     (4, dict(label='E', x=None, y=None, level=None)),
    #     (5, dict(label='E', x=None, y=None, level=None)),
    #     (6, dict(label='E', x=None, y=None, level=None))
    # ]

    # right_side_nodes = [right_side_parent_node] + right_side_nodes_new

    # right_side_edges = [
    #     (3,4), (3,6), (3,1), (4,5), (4,6), (4,1), (4,2), (5,2), (5,6), (6,1), (6,2), (parent_tmp_node_number,1), (parent_tmp_node_number,2),
    # ]

    # right_production_side = nx.Graph()
    # right_production_side.add_nodes_from(right_side_nodes)
    # right_production_side.add_edges_from(right_side_edges)


if __name__ == '__main__':
    graph = nx.Graph()
    graph.add_node(0, label='El', x=1.0, y=1.0, level=0)

    draw(graph, 'before.png')
    p1(graph)
    draw(graph, 'after_1.png')
    p2(graph)
    # draw(graph, 'after_2.png')


# [A,B,C,D,E]

# B = lambda l: return l[1] == l[0] + l[2] / 2
# D = C+E/2

# {
#     node_graph1: 3
# }