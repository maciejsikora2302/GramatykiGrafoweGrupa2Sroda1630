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
from p9 import p9
from p10 import p10
from p12 import p12


def old_main():
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


def wywod_1():
    graph = nx.Graph()
    LOW = 1.0
    HIGH = 40.0
    graph.add_node(0, label="El", x=0.0, y=0.0, level=0)
    draw(graph, filename="./wywod_1_draw/init.png")

    p1(graph, 0)
    print("p1 done")
    draw(graph, filename="./wywod_1_draw/step_1.png")

    p9(graph, 1)
    print("p9 done")
    draw(graph, filename="./wywod_1_draw/step_2.png")

    p9(graph, 1)
    print("p9 done")
    draw(graph, filename="./wywod_1_draw/step_3.png")

    p12(graph, 1)
    print("p12 done")
    draw(graph, filename="./wywod_1_draw/step_4.png")

    p2(graph, 2)
    print("p2 done")
    draw(graph, filename="./wywod_1_draw/step_5.png")

    p9(graph, 2)
    print("p9 done")
    draw(graph, filename="./wywod_1_draw/step_6.png")

    p10(graph, 2)
    print("p10 done")
    draw(graph, filename="./wywod_1_draw/step_7.png")

    save_graph(graph, "saved_graphs/graph.gexf")


if __name__ == "__main__":
    wywod_1()
