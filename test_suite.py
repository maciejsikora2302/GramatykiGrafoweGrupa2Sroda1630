import unittest
import networkx as nx

from p3 import p3
from p4 import p4
from p5 import p5
from p9 import p9

class P3_Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_should_do_nothing_when_no_isomorphic_subgraph_found(self):
        # given
        level = 2

        nodes = [
            (1, dict(label='E', x=0.0, y=1.0, level=level)),
            (2, dict(label='E', x=1.0, y=1.0, level=level)),
            (3, dict(label='E', x=1.0, y=0.0, level=level)),
            (4, dict(label='E', x=0.0, y=0.0, level=level)),
            (5, dict(label='I', x=1/3, y=2/3, level=level)),
            (6, dict(label='I', x=2/3, y=1/3, level=level))
        ]
        edges = [
            (1,2), (2,3), (3,4), (4,1), # boundary edges
            (2,4), # internal edge
            (1,5), (2,5), (4,5), # internal I node of triangle <1,2,4>
            (2,6), (3,6), (4,6)  # internal I node of triangle <2,3,4>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p3(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))
        self.assertEqual(G.nodes[5]['label'], 'I')
        self.assertEqual(G.nodes[6]['label'], 'I')

    def test_should_split_trianle_when_isomorphic_subgraph_found(self):
        # given
        level = 2

        nodes = [
            (1, dict(label='E', x=0.0, y=1.0, level=level)),
            (2, dict(label='E', x=1.0, y=1.0, level=level)),
            (3, dict(label='E', x=1.0, y=0.5, level=level)),
            (4, dict(label='E', x=1.0, y=0.0, level=level)),
            (5, dict(label='E', x=0.0, y=0.0, level=level)),
            (6, dict(label='I', x=1/3, y=2/3, level=level)),
            (7, dict(label='I', x=2/3, y=1/3, level=level))
        ]
        edges = [
            (1,2), (2,3), (3,4), (4,5), (5,1), # boundary edges
            (2,5), # internal edge
            (1,6), (2,6), (5,6), # internal I node of triangle <1,2,5>
            (2,7), (4,7), (5,7)  # internal I node of triangle <2,4,5>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p3(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes) + 6)
        self.assertEqual(len(G.edges), len(edges) + 11 + 2)
        self.assertEqual(G.nodes[6]['label'], 'I')
        self.assertEqual(G.nodes[7]['label'], 'i')

    def test_should_split_exactly_one_triangle_in_each_call(self):
        # given
        level = 2

        nodes = [
            (1, dict(label='E', x=0.0, y=1.0, level=level)),
            (2, dict(label='E', x=1.0, y=1.0, level=level)),
            (3, dict(label='E', x=1.0, y=0.0, level=level)),
            (4, dict(label='E', x=0.0, y=0.0, level=level)),
            (5, dict(label='E', x=0.5, y=0.5, level=level)),
            (6, dict(label='I', x=1/3, y=2/3, level=level)),
            (7, dict(label='I', x=2/3, y=1/3, level=level))
        ]
        edges = [
            (1,2), (2,3), (3,4), (4,1), # boundary edges
            (2,5), (5,4), # internal edges
            (1,6), (2,6), (4,6), # internal I node of triangle <1,2,4>
            (2,7), (3,7), (4,7)  # internal I node of triangle <2,3,4>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when-then: first-call
        p3(G, level)

        self.assertEqual(len(G.nodes), len(nodes) + 6)
        self.assertEqual(len(G.edges), len(edges) + 11 + 2)
        broken_triangles_cnt = sum([1 if G.nodes[x]['label'] == 'i' else 0 for x in [6, 7]])
        self.assertEqual(broken_triangles_cnt, 1)

        # when-then: second-call
        p3(G, level)

        self.assertEqual(len(G.nodes), len(nodes) + 6 * 2)
        self.assertEqual(len(G.edges), len(edges) + (11 + 2) * 2)
        self.assertEqual(G.nodes[6]['label'], 'i')
        self.assertEqual(G.nodes[7]['label'], 'i')

        # when-then: third-call (should not change)
        p3(G, level)

        self.assertEqual(len(G.nodes), len(nodes) + 6 * 2)
        self.assertEqual(len(G.edges), len(edges) + (11 + 2) * 2)
        self.assertEqual(G.nodes[6]['label'], 'i')
        self.assertEqual(G.nodes[7]['label'], 'i')

class P4_Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_should_do_nothing_when_no_isomorphic_subgraph_found(self):
        # given
        level = 2

        nodes = [
            (1, dict(label='E', x=0.0, y=1.0, level=level)),
            (2, dict(label='E', x=1.0, y=1.0, level=level)),
            (3, dict(label='E', x=1.0, y=0.5, level=level)),
            (4, dict(label='E', x=1.0, y=0.0, level=level)),
            (5, dict(label='E', x=0.0, y=0.0, level=level)),
            (6, dict(label='I', x=1/3, y=2/3, level=level)),
            (7, dict(label='I', x=2/3, y=1/3, level=level))
        ]
        edges = [
            (1,2), (2,3), (3,4), (4,5), (5,1), # boundary edges
            (2,5), # internal edge
            (1,6), (2,6), (5,6), # internal I node of triangle <1,2,5>
            (2,7), (4,7), (5,7)  # internal I node of triangle <2,4,5>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p4(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))
        self.assertEqual(G.nodes[6]['label'], 'I')
        self.assertEqual(G.nodes[7]['label'], 'I')

    def test_should_split_trianle_when_isomorphic_subgraph_found(self):
        # given
        level = 2

        nodes = [
            (1, dict(label='E', x=0.0, y=1.0, level=level)),
            (2, dict(label='E', x=1.0, y=1.0, level=level)),
            (3, dict(label='E', x=1.0, y=0.5, level=level)),
            (4, dict(label='E', x=1.0, y=0.0, level=level)),
            (5, dict(label='E', x=0.0, y=0.0, level=level)),
            (6, dict(label='I', x=1/3, y=2/3, level=level)),
            (7, dict(label='I', x=2/3, y=1/3, level=level)),
            (8, dict(label='E', x=0.5, y=0.5, level=level))
        ]
        edges = [
            (1,2), (2,3), (3,4), (4,5), (5,1), # boundary edges
            (2,8), (8,5), # internal edges
            (1,6), (2,6), (5,6), # internal I node of triangle <1,2,5>
            (2,7), (4,7), (5,7)  # internal I node of triangle <2,4,5>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p4(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes) + 8)
        self.assertEqual(len(G.edges), len(edges) + 16 + 3)
        self.assertEqual(G.nodes[6]['label'], 'I')
        self.assertEqual(G.nodes[7]['label'], 'i')
    
    def test_should_split_exactly_one_triangle_in_each_call(self):
        # given
        level = 2

        nodes = [
            (1, dict(label='E', x=0.0, y=1.0, level=level)),
            (2, dict(label='E', x=1.0, y=1.0, level=level)),
            (3, dict(label='E', x=1.0, y=0.5, level=level)),
            (4, dict(label='E', x=1.0, y=0.0, level=level)),
            (5, dict(label='E', x=0.0, y=0.0, level=level)),
            (6, dict(label='I', x=1/3, y=2/3, level=level)),
            (7, dict(label='I', x=2/3, y=1/3, level=level)),
            (8, dict(label='E', x=0.5, y=0.5, level=level)),
            (9, dict(label='E', x=0.0, y=0.5, level=level))
        ]
        edges = [
            (1,2), (2,3), (3,4), (4,5), (5,9), (9,1), # boundary edges
            (2,8), (8,5), # internal edges
            (1,6), (2,6), (5,6), # internal I node of triangle <1,2,5>
            (2,7), (4,7), (5,7)  # internal I node of triangle <2,4,5>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when-then: first-call
        p4(G, level)

        self.assertEqual(len(G.nodes), len(nodes) + 8)
        self.assertEqual(len(G.edges), len(edges) + 16 + 3)
        broken_triangles_cnt = sum([1 if G.nodes[x]['label'] == 'i' else 0 for x in [6, 7]])
        self.assertEqual(broken_triangles_cnt, 1)

        # when-then: second-call
        p4(G, level)

        self.assertEqual(len(G.nodes), len(nodes) + 8 * 2)
        self.assertEqual(len(G.edges), len(edges) + (16 + 3) * 2)
        self.assertEqual(G.nodes[6]['label'], 'i')
        self.assertEqual(G.nodes[7]['label'], 'i')

        # when-then: third-call (should not change)
        p4(G, level)

        self.assertEqual(len(G.nodes), len(nodes) + 8 * 2)
        self.assertEqual(len(G.edges), len(edges) + (16 + 3) * 2)
        self.assertEqual(G.nodes[6]['label'], 'i')
        self.assertEqual(G.nodes[7]['label'], 'i')

class P5_Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_should_split_triangle_when_isomorphic_subgraph_found(self):
        #given
        level = 2

        nodes = [
            (1, dict(label='E', x=0.0, y=1.0, level=level)),
            (2, dict(label='E', x=0.0, y=0.0, level=level)),
            (3, dict(label='E', x=1.0, y=0.0, level=level)),
            (4, dict(label='E', x=0.0, y=0.5, level=level)),
            (5, dict(label='E', x=0.5, y=0.0, level=level)),
            (6, dict(label='E', x=0.5, y=0.5, level=level)),
            (7, dict(label='I', x=1/3, y=2/3, level=level)),
            (8, dict(label='E', x=2/3, y=0.0, level=level)),
            (9, dict(label='I', x=1/3, y=1/3, level=level))
        ]
        edges = [
            (1,4), (4,2), (2,5), (5,3), (3,6), (6,1), # boundary edges
            (1,8), (2,8), # internal edges
            (1,7), (2,7), (3,7), # internal I node of triangle <1,2,3>
            (1,9), (2,9), (8,9)  # internal I node of triangle <1,2,8>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p5(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes) + 10)
        self.assertEqual(len(G.edges), len(edges) + 25)
        self.assertEqual(G.nodes[7]['label'], 'i')
        self.assertEqual(G.nodes[9]['label'], 'I')

    def test_should_not_split_when_constraints_not_met(self):
        #given
        level = 2

        nodes = [
            (1, dict(label='E', x=0.0, y=1.0, level=level)),
            (2, dict(label='E', x=0.0, y=0.0, level=level)),
            (3, dict(label='E', x=1.0, y=0.0, level=level)),
            (4, dict(label='E', x=0.0, y=0.5, level=level)),
            (5, dict(label='E', x=0.4, y=0.0, level=level)),
            (6, dict(label='E', x=0.5, y=0.5, level=level)),
            (7, dict(label='I', x=1/3, y=2/3, level=level)),
            (8, dict(label='E', x=2/3, y=0.0, level=level)),
            (9, dict(label='I', x=1/3, y=1/3, level=level))
        ]
        edges = [
            (1,4), (4,2), (2,5), (5,3), (3,6), (6,1), # boundary edges
            (1,8), (2,8), # internal edges
            (1,7), (2,7), (3,7), # internal I node of triangle <1,2,3>
            (1,9), (2,9), (8,9)  # internal I node of triangle <1,2,8>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p5(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))
        self.assertEqual(G.nodes[7]['label'], 'I')
        self.assertEqual(G.nodes[9]['label'], 'I')

    def test_should_not_split_when_constraints_not_met_deleted_node(self):
        #given
        level = 2

        nodes = [
            (1, dict(label='E', x=0.0, y=1.0, level=level)),
            (2, dict(label='E', x=0.0, y=0.0, level=level)),
            (3, dict(label='E', x=1.0, y=0.0, level=level)),
            (4, dict(label='E', x=0.0, y=0.5, level=level)),
            (6, dict(label='E', x=0.5, y=0.5, level=level)),
            (7, dict(label='I', x=1/3, y=2/3, level=level)),
            (8, dict(label='E', x=2/3, y=0.0, level=level)),
            (9, dict(label='I', x=1/3, y=1/3, level=level))
        ]
        edges = [
            (1,4), (4,2), (2,3), (3,6), (6,1), # boundary edges
            (1,8), (2,8), # internal edges
            (1,7), (2,7), (3,7), # internal I node of triangle <1,2,3>
            (1,9), (2,9), (8,9)  # internal I node of triangle <1,2,8>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p5(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))
        self.assertEqual(G.nodes[7]['label'], 'I')
        self.assertEqual(G.nodes[9]['label'], 'I')

    def test_should_not_split_when_constraints_not_met_edge_deleted(self):
        #given
        level = 2

        nodes = [
            (1, dict(label='E', x=0.0, y=1.0, level=level)),
            (2, dict(label='E', x=0.0, y=0.0, level=level)),
            (3, dict(label='E', x=1.0, y=0.0, level=level)),
            (4, dict(label='E', x=0.0, y=0.5, level=level)),
            (6, dict(label='E', x=0.5, y=0.5, level=level)),
            (7, dict(label='I', x=1/3, y=2/3, level=level)),
            (8, dict(label='E', x=2/3, y=0.0, level=level)),
            (9, dict(label='I', x=1/3, y=1/3, level=level))
        ]
        edges = [
            (1,4), (4,2), (3,6), (6,1), # boundary edges
            (1,8), (2,8), # internal edges
            (1,7), (2,7), (3,7), # internal I node of triangle <1,2,3>
            (1,9), (2,9), (8,9)  # internal I node of triangle <1,2,8>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p5(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))
        self.assertEqual(G.nodes[7]['label'], 'I')
        self.assertEqual(G.nodes[9]['label'], 'I')



class P9_Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_should_do_nothing_when_no_isomorphic_subgraph_found(self):
        # given
        level = 2

        nodes = [
            (1, dict(label='E', x=0.0, y=1.0, level=level)),
            (2, dict(label='E', x=1.0, y=1.0, level=level)),
            (3, dict(label='E', x=1.0, y=0.0, level=level)),
            (4, dict(label='E', x=0.0, y=0.0, level=level)),
            (5, dict(label='I', x=1/3, y=2/3, level=level)),
            (6, dict(label='I', x=2/3, y=1/3, level=level))
        ]
        edges = [
            (1,2), (2,3), (3,4), (4,1), # boundary edges
            (2,4), # internal edge
            (1,5), (2,5), #(4,5), # internal I node of triangle <1,2,4> with missing edge
            (2,6), (3,6), #(4,6)  # internal I node of triangle <2,3,4> with missing edge
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p9(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))
        self.assertEqual(G.nodes[5]['label'], 'I')
        self.assertEqual(G.nodes[6]['label'], 'I')

    def test_should_split_trianle_when_isomorphic_subgraph_found(self):
        # given
        level = 2

        nodes = [
            (1, dict(label='E', x=0.0, y=1.0, level=level)),
            (2, dict(label='E', x=1.0, y=1.0, level=level)),
            (3, dict(label='E', x=1.0, y=0.0, level=level)),
            (4, dict(label='E', x=0.0, y=0.0, level=level)),
            (5, dict(label='I', x=1/3, y=2/3, level=level)),
            (6, dict(label='I', x=2/3, y=1/3, level=level))
        ]
        edges = [
            (1,2), (2,3), (3,4), (4,1), # boundary edges
            (2,4), # internal edge
            (1,5), (2,5), (4,5), # internal I node of triangle <1,2,4>
            (2,6), (3,6), (4,6)  # internal I node of triangle <2,3,4>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p9(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes) + 4)
        self.assertEqual(len(G.edges), len(edges) + 7)
        # One of the two should be split
    def test_should_do_nothing_when_no_starting_nodes_found(self):
        # given
        level = 2

        nodes = [
            (1, dict(label='E', x=0.0, y=1.0, level=level)),
            (2, dict(label='E', x=1.0, y=1.0, level=level)),
            (3, dict(label='E', x=1.0, y=0.0, level=level)),
            (4, dict(label='E', x=0.0, y=0.0, level=level)),
            (5, dict(label='E', x=1/3, y=2/3, level=level)),
            (6, dict(label='E', x=2/3, y=1/3, level=level))
        ]
        edges = [
            (1,2), (2,3), (3,4), (4,1), # boundary edges
            (2,4), # internal edge
            (1,5), (2,5), (4,5), # internal I node of triangle <1,2,4>
            (2,6), (3,6), (4,6)  # internal I node of triangle <2,3,4>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p9(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))
        self.assertEqual(G.nodes[5]['label'], 'E')
        self.assertEqual(G.nodes[6]['label'], 'E')

    def test_should_do_nothing_when_extra_nodes_found(self):
        # given
        level = 2

        nodes = [
            (1, dict(label='E', x=0.0, y=1.0, level=level)),
            (2, dict(label='E', x=1.0, y=1.0, level=level)),
            (3, dict(label='E', x=0.0, y=0.0, level=level)),
            (4, dict(label='I', x=1 / 3, y=2 / 3, level=level)),
            (5, dict(label='E', x=1 / 2, y=1 / 2, level=level))
        ]
        edges = [
            (1, 2), (2, 5), (5, 3), (3, 1),  # boundary edges
            (1, 4), (2, 4), (3, 4)  # internal I node of triangle <1,2,3>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p9(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))
        self.assertEqual(G.nodes[4]['label'], 'I')
        self.assertEqual(G.nodes[5]['label'], 'E')


if __name__ == '__main__':
    unittest.main()
