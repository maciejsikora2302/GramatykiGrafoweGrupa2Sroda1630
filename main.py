"""
Proszę założyć projekt na githubie, udostępnić go studentom z grupy oraz
zaimplementować produkcję (P1) i (P2) wraz z wizualizacją grafu wykorzystując
współrzędne wierzchołków i umożliwiając wybór poziomu grafu do wizualizacji.
Proszę napisać testy jednostkowe do produkcji (P1) i (P2) oraz do wizualizacji
grafu oraz umieścić produkcję oraz testy w githubie
"""


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
from pprint import pprint as pp
from general_utils import draw, save_graph

from p1 import p1
from p2 import p2
from p3 import p3
from p4 import p4

if __name__ == "__main__":
    graph = nx.Graph()
    graph.add_node(0, label="El", x=0.5, y=0.5, level=0)

    draw(graph, filename="./dev_draw/before.png")
    p1(graph, 0)
    draw(graph, filename="./dev_draw/after_1.png")
    p2(graph, 1)
    draw(graph, filename="./dev_draw/after_2.png")
    p2(graph, 1)
    draw(graph, filename="./dev_draw/after_3.png")

    save_graph(graph, "saved_graphs/graph.gexf")
