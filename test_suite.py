import unittest
import networkx as nx


from p1 import p1
from p2 import p2
from p3 import p3
from p4 import p4
from p5 import p5

class P1_Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_should_add_starting_graph(self):
        # given
        level = 0

        nodes = [
            (1, dict(label='El', x=1.0, y=1.0, level=level))
        ]
        edges = [
            
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        LOW = 1.0
        HIGH = 40.0
        p1(G, level, LOW, HIGH)

        # then
        self.assertEqual(len(G.nodes), len(nodes) + 6)
        self.assertEqual(len(G.edges), len(edges) + 13)

        # check labels
        self.assertEqual(G.nodes[1]['label'], 'el')
        self.assertEqual(G.nodes[2]['label'], 'I')
        self.assertEqual(G.nodes[3]['label'], 'I')
        self.assertEqual(G.nodes[4]['label'], 'E')
        self.assertEqual(G.nodes[5]['label'], 'E')
        self.assertEqual(G.nodes[6]['label'], 'E')
        self.assertEqual(G.nodes[7]['label'], 'E')

        # check coordinates
        self.assertEqual(G.nodes[2]['x'], (2*LOW+HIGH)/3)
        self.assertEqual(G.nodes[2]['y'], (2*LOW+HIGH)/3)
        self.assertEqual(G.nodes[3]['x'], (LOW+2*HIGH)/3)
        self.assertEqual(G.nodes[3]['y'], (LOW+2*HIGH)/3)
        self.assertEqual(G.nodes[4]['x'], LOW)
        self.assertEqual(G.nodes[4]['y'], LOW)
        self.assertEqual(G.nodes[5]['x'], HIGH)
        self.assertEqual(G.nodes[5]['y'], LOW)
        self.assertEqual(G.nodes[6]['x'], HIGH)
        self.assertEqual(G.nodes[6]['y'], HIGH)
        self.assertEqual(G.nodes[7]['x'], LOW)
        self.assertEqual(G.nodes[7]['y'], HIGH)
      
    def test_should_add_starting_graph_when_multiple_starting_points_are_avaiable(self):
        # given
        level = 0

        nodes = [
            (1, dict(label='El', x=1.0, y=1.0, level=level)),
            (2, dict(label='El', x=1.0, y=1.0, level=level)),
        ]
        edges = [
            (1,2)
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        LOW = 1.0
        HIGH = 40.0
        p1(G, level, LOW, HIGH)

        # then
        self.assertEqual(len(G.nodes), len(nodes) + 6)
        self.assertEqual(len(G.edges), len(edges) + 13)

        # check labels
        self.assertEqual(G.nodes[1]['label'], 'el')
        self.assertEqual(G.nodes[2]['label'], 'El')
        self.assertEqual(G.nodes[3]['label'], 'I')
        self.assertEqual(G.nodes[4]['label'], 'I')
        self.assertEqual(G.nodes[5]['label'], 'E')
        self.assertEqual(G.nodes[6]['label'], 'E')
        self.assertEqual(G.nodes[7]['label'], 'E')
        self.assertEqual(G.nodes[8]['label'], 'E')

        # check coordinates
        self.assertEqual(G.nodes[3]['x'], (2*LOW+HIGH)/3)
        self.assertEqual(G.nodes[3]['y'], (2*LOW+HIGH)/3)
        self.assertEqual(G.nodes[4]['x'], (LOW+2*HIGH)/3)
        self.assertEqual(G.nodes[4]['y'], (LOW+2*HIGH)/3)
        self.assertEqual(G.nodes[5]['x'], LOW)
        self.assertEqual(G.nodes[5]['y'], LOW)
        self.assertEqual(G.nodes[6]['x'], HIGH)
        self.assertEqual(G.nodes[6]['y'], LOW)
        self.assertEqual(G.nodes[7]['x'], HIGH)
        self.assertEqual(G.nodes[7]['y'], HIGH)
        self.assertEqual(G.nodes[8]['x'], LOW)
        self.assertEqual(G.nodes[8]['y'], HIGH)


    #więcej niż jeden wierzchołek


class P2_Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_should_add_subgraph_when_isomorphic_subgraph_is_found(self):
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

        #add couple of nodes to  nodes list
        nodes.append((7, dict(label='E', x=0.0, y=1.0, level=level)))
        nodes.append((8, dict(label='E', x=1.0, y=1.0, level=level)))
        nodes.append((9, dict(label='E', x=1.0, y=0.0, level=level)))

        #and edges between them
        edges.append((7,8))
        edges.append((8,9))
        edges.append((9,7))


        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p2(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes) + 6)
        self.assertEqual(len(G.edges), len(edges) + 13)

        # check labels
        self.assertEqual(G.nodes[1]['label'], 'E')
        self.assertEqual(G.nodes[2]['label'], 'E')
        self.assertEqual(G.nodes[3]['label'], 'E')
        self.assertEqual(G.nodes[4]['label'], 'E')
        self.assertEqual(G.nodes[5]['label'], 'i')
        self.assertEqual(G.nodes[6]['label'], 'I')
        self.assertEqual(G.nodes[7]['label'], 'E')
        self.assertEqual(G.nodes[8]['label'], 'E')
        self.assertEqual(G.nodes[9]['label'], 'E')
        self.assertEqual(G.nodes[10]['label'], 'I')
        self.assertEqual(G.nodes[11]['label'], 'I')

        # check coordinates
        self.assertEqual(G.nodes[5]['x'], 1/3)
        self.assertEqual(G.nodes[5]['y'], 2/3)
        self.assertEqual(G.nodes[6]['x'], 2/3)
        self.assertEqual(G.nodes[6]['y'], 1/3)
        self.assertEqual(G.nodes[10]['x'], 1/3)
        self.assertEqual(G.nodes[10]['y'], 2/3)
        self.assertEqual(G.nodes[11]['x'], 1/3)
        self.assertEqual(G.nodes[11]['y'], 1/2)
        

    def test_should_do_notihng_when_no_isomorphinc_subgraph_found(self):
        # given
        level = 2

        nodes = [
            (1, dict(label='E', x=0.0, y=1.0, level=level)),
            (2, dict(label='E', x=1.0, y=1.0, level=level)),
            (3, dict(label='E', x=1.0, y=0.0, level=level)),
            (4, dict(label='E', x=0.0, y=0.0, level=level))
        ]
        edges = [
            (1,2), (2,3), (3,4), 
            (2,4), 
            (1,4),
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # print(G)
        # when
        p2(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))

        # check labels
        self.assertEqual(G.nodes[1]['label'], 'E')
        self.assertEqual(G.nodes[2]['label'], 'E')
        self.assertEqual(G.nodes[3]['label'], 'E')
        self.assertEqual(G.nodes[4]['label'], 'E')
        

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

class P5_Test():
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

if __name__ == '__main__':
    unittest.main()
