import unittest
import networkx as nx

from parameterized import parameterized

from p1 import p1
from p2 import p2
from p3 import p3
from p4 import p4
from p5 import p5
from p6 import p6
from p9 import p9
from p10 import p10


class P1_Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_should_add_starting_graph(self):
        # given
        level = 0

        nodes = [(1, dict(label="El", x=1.0, y=1.0, level=level))]
        edges = []

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
        self.assertEqual(G.nodes[1]["label"], "el")
        self.assertEqual(G.nodes[2]["label"], "I")
        self.assertEqual(G.nodes[3]["label"], "I")
        self.assertEqual(G.nodes[4]["label"], "E")
        self.assertEqual(G.nodes[5]["label"], "E")
        self.assertEqual(G.nodes[6]["label"], "E")
        self.assertEqual(G.nodes[7]["label"], "E")

        # check coordinates
        self.assertEqual(G.nodes[2]["x"], (2 * LOW + HIGH) / 3)
        self.assertEqual(G.nodes[2]["y"], (2 * LOW + HIGH) / 3)
        self.assertEqual(G.nodes[3]["x"], (LOW + 2 * HIGH) / 3)
        self.assertEqual(G.nodes[3]["y"], (LOW + 2 * HIGH) / 3)
        self.assertEqual(G.nodes[4]["x"], LOW)
        self.assertEqual(G.nodes[4]["y"], LOW)
        self.assertEqual(G.nodes[5]["x"], HIGH)
        self.assertEqual(G.nodes[5]["y"], LOW)
        self.assertEqual(G.nodes[6]["x"], HIGH)
        self.assertEqual(G.nodes[6]["y"], HIGH)
        self.assertEqual(G.nodes[7]["x"], LOW)
        self.assertEqual(G.nodes[7]["y"], HIGH)

    def test_should_add_starting_graph_when_multiple_starting_points_are_avaiable(self):
        # given
        level = 0

        nodes = [
            (1, dict(label="El", x=1.0, y=1.0, level=level)),
            (2, dict(label="El", x=1.0, y=1.0, level=level)),
        ]
        edges = [(1, 2)]

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
        self.assertEqual(G.nodes[1]["label"], "el")
        self.assertEqual(G.nodes[2]["label"], "El")
        self.assertEqual(G.nodes[3]["label"], "I")
        self.assertEqual(G.nodes[4]["label"], "I")
        self.assertEqual(G.nodes[5]["label"], "E")
        self.assertEqual(G.nodes[6]["label"], "E")
        self.assertEqual(G.nodes[7]["label"], "E")
        self.assertEqual(G.nodes[8]["label"], "E")

        # check coordinates
        self.assertEqual(G.nodes[3]["x"], (2 * LOW + HIGH) / 3)
        self.assertEqual(G.nodes[3]["y"], (2 * LOW + HIGH) / 3)
        self.assertEqual(G.nodes[4]["x"], (LOW + 2 * HIGH) / 3)
        self.assertEqual(G.nodes[4]["y"], (LOW + 2 * HIGH) / 3)
        self.assertEqual(G.nodes[5]["x"], LOW)
        self.assertEqual(G.nodes[5]["y"], LOW)
        self.assertEqual(G.nodes[6]["x"], HIGH)
        self.assertEqual(G.nodes[6]["y"], LOW)
        self.assertEqual(G.nodes[7]["x"], HIGH)
        self.assertEqual(G.nodes[7]["y"], HIGH)
        self.assertEqual(G.nodes[8]["x"], LOW)
        self.assertEqual(G.nodes[8]["y"], HIGH)


class P2_Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_should_add_subgraph_when_isomorphic_subgraph_is_found(self):
        # given
        level = 2

        nodes = [
            (1, dict(label="E", x=0.0, y=1.0, level=level)),
            (2, dict(label="E", x=1.0, y=1.0, level=level)),
            (3, dict(label="E", x=1.0, y=0.0, level=level)),
            (4, dict(label="E", x=0.0, y=0.0, level=level)),
            (5, dict(label="I", x=1 / 3, y=2 / 3, level=level)),
            (6, dict(label="I", x=2 / 3, y=1 / 3, level=level)),
        ]
        edges = [
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 1),  # boundary edges
            (2, 4),  # internal edge
            (1, 5),
            (2, 5),
            (4, 5),  # internal I node of triangle <1,2,4>
            (2, 6),
            (3, 6),
            (4, 6),  # internal I node of triangle <2,3,4>
        ]

        # add couple of nodes to  nodes list
        nodes.append((7, dict(label="E", x=0.0, y=1.0, level=level)))
        nodes.append((8, dict(label="E", x=1.0, y=1.0, level=level)))
        nodes.append((9, dict(label="E", x=1.0, y=0.0, level=level)))

        # and edges between them
        edges.append((7, 8))
        edges.append((8, 9))
        edges.append((9, 7))

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p2(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes) + 6)
        self.assertEqual(len(G.edges), len(edges) + 13)

        # check labels
        self.assertEqual(G.nodes[1]["label"], "E")
        self.assertEqual(G.nodes[2]["label"], "E")
        self.assertEqual(G.nodes[3]["label"], "E")
        self.assertEqual(G.nodes[4]["label"], "E")
        self.assertEqual(G.nodes[5]["label"], "i")
        self.assertEqual(G.nodes[6]["label"], "I")
        self.assertEqual(G.nodes[7]["label"], "E")
        self.assertEqual(G.nodes[8]["label"], "E")
        self.assertEqual(G.nodes[9]["label"], "E")
        self.assertEqual(G.nodes[10]["label"], "I")
        self.assertEqual(G.nodes[11]["label"], "I")

        # check coordinates
        self.assertEqual(G.nodes[5]["x"], 1 / 3)
        self.assertEqual(G.nodes[5]["y"], 2 / 3)
        self.assertEqual(G.nodes[6]["x"], 2 / 3)
        self.assertEqual(G.nodes[6]["y"], 1 / 3)
        self.assertEqual(G.nodes[10]["x"], 1 / 3)
        self.assertEqual(G.nodes[10]["y"], 2 / 3)
        self.assertEqual(G.nodes[11]["x"], 1 / 3)
        self.assertEqual(G.nodes[11]["y"], 1 / 2)

    def base_p2_isomorphic_graph(self):
        # given
        level = 2

        nodes = [
            (1, dict(label="E", x=0.0, y=1.0, level=level)),
            (2, dict(label="E", x=1.0, y=1.0, level=level)),
            (4, dict(label="E", x=0.0, y=0.0, level=level)),
            (5, dict(label="I", x=1 / 3, y=2 / 3, level=level)),
            (6, dict(label="I", x=2 / 3, y=1 / 3, level=level)),
        ]
        edges = [
            (1, 2),
            (4, 1),  # boundary edges
            (2, 4),  # internal edge
            (1, 5),
            (2, 5),
            (4, 5),  # internal I node of triangle <1,2,4>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        return G

    def test_should_apply_p2_to_base_p2_isomorphic_graph(self):
        # given
        G = self.base_p2_isomorphic_graph()
        # G.remove_node(3)
        level = 2

        # when
        G_copy = G.copy()
        p2(G_copy, level)

        # then
        self.assertNotEqual(G_copy.nodes, G.nodes)
        self.assertNotEqual(G_copy.edges, G.edges)

    @parameterized.expand([["1", 1], ["2", 2], ["4", 4], ["5", 5]])
    def test_should_do_nothing_when_no_isomorphic_subgraph_found(
        self, _test_name: str, node_to_remove: int
    ):
        # given
        G = self.base_p2_isomorphic_graph()
        G.remove_node(node_to_remove)
        level = 2

        # when
        G_copy = G.copy()
        p2(G_copy, level)

        # then
        self.assertEqual(G_copy.nodes, G.nodes)
        self.assertEqual(G_copy.edges, G.edges)


class P3_Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_should_do_nothing_when_no_isomorphic_subgraph_found(self):
        # given
        level = 2

        nodes = [
            (1, dict(label="E", x=0.0, y=1.0, level=level)),
            (2, dict(label="E", x=1.0, y=1.0, level=level)),
            (3, dict(label="E", x=1.0, y=0.0, level=level)),
            (4, dict(label="E", x=0.0, y=0.0, level=level)),
            (5, dict(label="I", x=1 / 3, y=2 / 3, level=level)),
            (6, dict(label="I", x=2 / 3, y=1 / 3, level=level)),
        ]
        edges = [
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 1),  # boundary edges
            (2, 4),  # internal edge
            (1, 5),
            (2, 5),
            (4, 5),  # internal I node of triangle <1,2,4>
            (2, 6),
            (3, 6),
            (4, 6),  # internal I node of triangle <2,3,4>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p3(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))
        self.assertEqual(G.nodes[5]["label"], "I")
        self.assertEqual(G.nodes[6]["label"], "I")

    def test_should_split_trianle_when_isomorphic_subgraph_found(self):
        # given
        level = 2

        nodes = [
            (1, dict(label="E", x=0.0, y=1.0, level=level)),
            (2, dict(label="E", x=1.0, y=1.0, level=level)),
            (3, dict(label="E", x=1.0, y=0.5, level=level)),
            (4, dict(label="E", x=1.0, y=0.0, level=level)),
            (5, dict(label="E", x=0.0, y=0.0, level=level)),
            (6, dict(label="I", x=1 / 3, y=2 / 3, level=level)),
            (7, dict(label="I", x=2 / 3, y=1 / 3, level=level)),
        ]
        edges = [
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 5),
            (5, 1),  # boundary edges
            (2, 5),  # internal edge
            (1, 6),
            (2, 6),
            (5, 6),  # internal I node of triangle <1,2,5>
            (2, 7),
            (4, 7),
            (5, 7),  # internal I node of triangle <2,4,5>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p3(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes) + 6)
        self.assertEqual(len(G.edges), len(edges) + 11 + 2)
        self.assertEqual(G.nodes[6]["label"], "I")
        self.assertEqual(G.nodes[7]["label"], "i")

    def test_should_split_exactly_one_triangle_in_each_call(self):
        # given
        level = 2

        nodes = [
            (1, dict(label="E", x=0.0, y=1.0, level=level)),
            (2, dict(label="E", x=1.0, y=1.0, level=level)),
            (3, dict(label="E", x=1.0, y=0.0, level=level)),
            (4, dict(label="E", x=0.0, y=0.0, level=level)),
            (5, dict(label="E", x=0.5, y=0.5, level=level)),
            (6, dict(label="I", x=1 / 3, y=2 / 3, level=level)),
            (7, dict(label="I", x=2 / 3, y=1 / 3, level=level)),
        ]
        edges = [
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 1),  # boundary edges
            (2, 5),
            (5, 4),  # internal edges
            (1, 6),
            (2, 6),
            (4, 6),  # internal I node of triangle <1,2,4>
            (2, 7),
            (3, 7),
            (4, 7),  # internal I node of triangle <2,3,4>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when-then: first-call
        p3(G, level)

        self.assertEqual(len(G.nodes), len(nodes) + 6)
        self.assertEqual(len(G.edges), len(edges) + 11 + 2)
        broken_triangles_cnt = sum(
            [1 if G.nodes[x]["label"] == "i" else 0 for x in [6, 7]]
        )
        self.assertEqual(broken_triangles_cnt, 1)

        # when-then: second-call
        p3(G, level)

        self.assertEqual(len(G.nodes), len(nodes) + 6 * 2)
        self.assertEqual(len(G.edges), len(edges) + (11 + 2) * 2)
        self.assertEqual(G.nodes[6]["label"], "i")
        self.assertEqual(G.nodes[7]["label"], "i")

        # when-then: third-call (should not change)
        p3(G, level)

        self.assertEqual(len(G.nodes), len(nodes) + 6 * 2)
        self.assertEqual(len(G.edges), len(edges) + (11 + 2) * 2)
        self.assertEqual(G.nodes[6]["label"], "i")
        self.assertEqual(G.nodes[7]["label"], "i")

    @parameterized.expand(
        [
            # name removed-nodes removed-edges (changed-node new-xy new-level)
            ("I-nodes removed", [6, 7], [], None),
            ("E-node removed", [2], [], None),
            ("E-node removed", [3], [], None),
            ("E-node removed", [4], [], None),
            ("E-node removed", [5], [], None),
            ("boundary edge removed", [], [(2, 3)], None),
            ("internal edge removed", [], [(2, 5)], None),
            ("internal I edges removed", [], [(1, 6), (4, 7)], None),
            ("changed level of a node", [], [], (5, None, 1)),
            ("changed position of a broken node", [], [], (3, (1.0, 0.4), None)),
        ]
    )
    def test_should_do_nothing_when_isomorphic_subgraph_is_broken(
        self, _name, removed_nodes, removed_edges, update
    ):
        # given
        level = 2

        nodes = [
            (1, dict(label="E", x=0.0, y=1.0, level=level)),
            (2, dict(label="E", x=1.0, y=1.0, level=level)),
            (3, dict(label="E", x=1.0, y=0.5, level=level)),
            (4, dict(label="E", x=1.0, y=0.0, level=level)),
            (5, dict(label="E", x=0.0, y=0.0, level=level)),
            (6, dict(label="I", x=1 / 3, y=2 / 3, level=level)),
            (7, dict(label="I", x=2 / 3, y=1 / 3, level=level)),
        ]
        edges = [
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 5),
            (5, 1),  # boundary edges
            (2, 5),  # internal edge
            (1, 6),
            (2, 6),
            (5, 6),  # internal I node of triangle <1,2,5>
            (2, 7),
            (4, 7),
            (5, 7),  # internal I node of triangle <2,4,5>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        for removed_node in removed_nodes:
            G.remove_node(removed_node)
            nodes = list(filter(lambda n: n[0] != removed_node, nodes))
            edges = list(filter(lambda e: removed_node not in e, edges))

        for removed_edge in removed_edges:
            G.remove_edge(*removed_edge)
            edges.remove(removed_edge)

        if update:
            idx, new_xy, new_level = update
            if new_xy:
                x, y = new_xy
                attrs = nx.get_node_attributes(G, "x")
                attrs[idx] = x
                nx.set_node_attributes(G, attrs, "x")
                attrs = nx.get_node_attributes(G, "y")
                attrs[idx] = y
                nx.set_node_attributes(G, attrs, "y")
            if new_level:
                attrs = nx.get_node_attributes(G, "level")
                attrs[idx] = new_level
                nx.set_node_attributes(G, attrs, "level")

        # when
        p3(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))

        I_node_count = sum(map(lambda n: n[1]["label"] == "I", nodes))
        self.assertTrue(
            I_node_count in (0, 2)
        )  # we either removed all of the I-nodes or they were unchanged
        self.assertTrue(
            all(map(lambda n: n[1]["label"] in ("E", "I"), G.nodes(data=True)))
        )  # The labels shouldn't change

    def test_should_not_modify_the_graph_meeting_criteria_for_p4(self):
        # given
        level = 2

        nodes = [
            (1, dict(label="E", x=0.0, y=1.0, level=level)),
            (2, dict(label="E", x=1.0, y=1.0, level=level)),
            (3, dict(label="E", x=1.0, y=0.5, level=level)),
            (4, dict(label="E", x=1.0, y=0.0, level=level)),
            (5, dict(label="E", x=0.0, y=0.0, level=level)),
            (6, dict(label="I", x=1 / 3, y=2 / 3, level=level)),
            (7, dict(label="I", x=2 / 3, y=1 / 3, level=level)),
            (8, dict(label="E", x=0.5, y=0.5, level=level)),
            (9, dict(label="E", x=0.0, y=0.5, level=level)),
        ]
        edges = [
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 5),
            (5, 9),
            (9, 1),  # boundary edges
            (2, 8),
            (8, 5),  # internal edges
            (1, 6),
            (2, 6),
            (5, 6),  # internal I node of triangle <1,2,5>
            (2, 7),
            (4, 7),
            (5, 7),  # internal I node of triangle <2,4,5>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when-then (p3 ~ no changes)
        p3(G, level)

        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))
        self.assertEqual(G.nodes[6]["label"], "I")
        self.assertEqual(G.nodes[7]["label"], "I")

        # when-then (p4 ~ changes)
        p4(G, level)

        self.assertEqual(len(G.nodes), len(nodes) + 8)
        self.assertEqual(len(G.edges), len(edges) + 16 + 3)
        broken_triangles_cnt = sum(
            [1 if G.nodes[x]["label"] == "i" else 0 for x in [6, 7]]
        )
        self.assertEqual(broken_triangles_cnt, 1)


class P4_Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_should_do_nothing_when_no_isomorphic_subgraph_found(self):
        # given
        level = 2

        nodes = [
            (1, dict(label="E", x=0.0, y=1.0, level=level)),
            (2, dict(label="E", x=1.0, y=1.0, level=level)),
            (3, dict(label="E", x=1.0, y=0.5, level=level)),
            (4, dict(label="E", x=1.0, y=0.0, level=level)),
            (5, dict(label="E", x=0.0, y=0.0, level=level)),
            (6, dict(label="I", x=1 / 3, y=2 / 3, level=level)),
            (7, dict(label="I", x=2 / 3, y=1 / 3, level=level)),
        ]
        edges = [
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 5),
            (5, 1),  # boundary edges
            (2, 5),  # internal edge
            (1, 6),
            (2, 6),
            (5, 6),  # internal I node of triangle <1,2,5>
            (2, 7),
            (4, 7),
            (5, 7),  # internal I node of triangle <2,4,5>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p4(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))
        self.assertEqual(G.nodes[6]["label"], "I")
        self.assertEqual(G.nodes[7]["label"], "I")

    def test_should_split_trianle_when_isomorphic_subgraph_found(self):
        # given
        level = 2

        nodes = [
            (1, dict(label="E", x=0.0, y=1.0, level=level)),
            (2, dict(label="E", x=1.0, y=1.0, level=level)),
            (3, dict(label="E", x=1.0, y=0.5, level=level)),
            (4, dict(label="E", x=1.0, y=0.0, level=level)),
            (5, dict(label="E", x=0.0, y=0.0, level=level)),
            (6, dict(label="I", x=1 / 3, y=2 / 3, level=level)),
            (7, dict(label="I", x=2 / 3, y=1 / 3, level=level)),
            (8, dict(label="E", x=0.5, y=0.5, level=level)),
        ]
        edges = [
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 5),
            (5, 1),  # boundary edges
            (2, 8),
            (8, 5),  # internal edges
            (1, 6),
            (2, 6),
            (5, 6),  # internal I node of triangle <1,2,5>
            (2, 7),
            (4, 7),
            (5, 7),  # internal I node of triangle <2,4,5>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p4(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes) + 8)
        self.assertEqual(len(G.edges), len(edges) + 16 + 3)
        self.assertEqual(G.nodes[6]["label"], "I")
        self.assertEqual(G.nodes[7]["label"], "i")

    def test_should_split_exactly_one_triangle_in_each_call(self):
        # given
        level = 2

        nodes = [
            (1, dict(label="E", x=0.0, y=1.0, level=level)),
            (2, dict(label="E", x=1.0, y=1.0, level=level)),
            (3, dict(label="E", x=1.0, y=0.5, level=level)),
            (4, dict(label="E", x=1.0, y=0.0, level=level)),
            (5, dict(label="E", x=0.0, y=0.0, level=level)),
            (6, dict(label="I", x=1 / 3, y=2 / 3, level=level)),
            (7, dict(label="I", x=2 / 3, y=1 / 3, level=level)),
            (8, dict(label="E", x=0.5, y=0.5, level=level)),
            (9, dict(label="E", x=0.0, y=0.5, level=level)),
        ]
        edges = [
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 5),
            (5, 9),
            (9, 1),  # boundary edges
            (2, 8),
            (8, 5),  # internal edges
            (1, 6),
            (2, 6),
            (5, 6),  # internal I node of triangle <1,2,5>
            (2, 7),
            (4, 7),
            (5, 7),  # internal I node of triangle <2,4,5>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when-then: first-call
        p4(G, level)

        self.assertEqual(len(G.nodes), len(nodes) + 8)
        self.assertEqual(len(G.edges), len(edges) + 16 + 3)
        broken_triangles_cnt = sum(
            [1 if G.nodes[x]["label"] == "i" else 0 for x in [6, 7]]
        )
        self.assertEqual(broken_triangles_cnt, 1)

        # when-then: second-call
        p4(G, level)

        self.assertEqual(len(G.nodes), len(nodes) + 8 * 2)
        self.assertEqual(len(G.edges), len(edges) + (16 + 3) * 2)
        self.assertEqual(G.nodes[6]["label"], "i")
        self.assertEqual(G.nodes[7]["label"], "i")

        # when-then: third-call (should not change)
        p4(G, level)

        self.assertEqual(len(G.nodes), len(nodes) + 8 * 2)
        self.assertEqual(len(G.edges), len(edges) + (16 + 3) * 2)
        self.assertEqual(G.nodes[6]["label"], "i")
        self.assertEqual(G.nodes[7]["label"], "i")

    @parameterized.expand(
        [
            # name removed-nodes removed-edges (changed-node new-xy new-level)
            ("I-nodes removed", [6, 7], [], None),
            ("E-node removed", [2], [], None),
            ("E-node removed", [3], [], None),
            ("E-node removed", [4], [], None),
            ("E-node removed", [5], [], None),
            ("E-node removed", [8], [], None),
            ("boundary edge removed", [], [(2, 3)], None),
            ("internal edge removed", [], [(2, 8)], None),
            ("internal I edges removed", [], [(1, 6), (4, 7)], None),
            ("changed level of a node", [], [], (8, None, 1)),
            ("changed position of a broken node", [], [], (3, (1.0, 0.4), None)),
            ("changed position of a broken node", [], [], (8, (0.4, 0.5), None)),
        ]
    )
    def test_should_do_nothing_when_isomorphic_subgraph_is_broken(
        self, _name, removed_nodes, removed_edges, update
    ):
        # given
        level = 2

        nodes = [
            (1, dict(label="E", x=0.0, y=1.0, level=level)),
            (2, dict(label="E", x=1.0, y=1.0, level=level)),
            (3, dict(label="E", x=1.0, y=0.5, level=level)),
            (4, dict(label="E", x=1.0, y=0.0, level=level)),
            (5, dict(label="E", x=0.0, y=0.0, level=level)),
            (6, dict(label="I", x=1 / 3, y=2 / 3, level=level)),
            (7, dict(label="I", x=2 / 3, y=1 / 3, level=level)),
            (8, dict(label="E", x=0.5, y=0.5, level=level)),
        ]
        edges = [
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 5),
            (5, 1),  # boundary edges
            (2, 8),
            (8, 5),  # internal edges
            (1, 6),
            (2, 6),
            (5, 6),  # internal I node of triangle <1,2,5>
            (2, 7),
            (4, 7),
            (5, 7),  # internal I node of triangle <2,4,5>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        for removed_node in removed_nodes:
            G.remove_node(removed_node)
            nodes = list(filter(lambda n: n[0] != removed_node, nodes))
            edges = list(filter(lambda e: removed_node not in e, edges))

        for removed_edge in removed_edges:
            G.remove_edge(*removed_edge)
            edges.remove(removed_edge)

        if update:
            idx, new_xy, new_level = update
            if new_xy:
                x, y = new_xy
                attrs = nx.get_node_attributes(G, "x")
                attrs[idx] = x
                nx.set_node_attributes(G, attrs, "x")
                attrs = nx.get_node_attributes(G, "y")
                attrs[idx] = y
                nx.set_node_attributes(G, attrs, "y")
            if new_level:
                attrs = nx.get_node_attributes(G, "level")
                attrs[idx] = new_level
                nx.set_node_attributes(G, attrs, "level")

        # when
        p4(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))

        I_node_count = sum(map(lambda n: n[1]["label"] == "I", nodes))
        self.assertTrue(
            I_node_count in (0, 2)
        )  # we either removed all of the I-nodes or they were unchanged
        self.assertTrue(
            all(map(lambda n: n[1]["label"] in ("E", "I"), G.nodes(data=True)))
        )  # The labels shouldn't change

    def test_should_not_modify_the_graph_meeting_criteria_for_p3(self):
        # given
        level = 2

        nodes = [
            (1, dict(label="E", x=0.0, y=1.0, level=level)),
            (2, dict(label="E", x=1.0, y=1.0, level=level)),
            (3, dict(label="E", x=1.0, y=0.5, level=level)),
            (4, dict(label="E", x=1.0, y=0.0, level=level)),
            (5, dict(label="E", x=0.0, y=0.0, level=level)),
            (6, dict(label="I", x=1 / 3, y=2 / 3, level=level)),
            (7, dict(label="I", x=2 / 3, y=1 / 3, level=level)),
        ]
        edges = [
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 5),
            (5, 1),  # boundary edges
            (2, 5),  # internal edge
            (1, 6),
            (2, 6),
            (5, 6),  # internal I node of triangle <1,2,5>
            (2, 7),
            (4, 7),
            (5, 7),  # internal I node of triangle <2,4,5>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when-then (p4 ~ no changes)
        p4(G, level)

        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))
        self.assertEqual(G.nodes[6]["label"], "I")
        self.assertEqual(G.nodes[7]["label"], "I")

        # when-then (p3 ~ changes)
        p3(G, level)

        self.assertEqual(len(G.nodes), len(nodes) + 6)
        self.assertEqual(len(G.edges), len(edges) + 11 + 2)
        self.assertEqual(G.nodes[6]["label"], "I")
        self.assertEqual(G.nodes[7]["label"], "i")


class P5_Test:
    def setUp(self):
        pass

    def test_should_split_triangle_when_isomorphic_subgraph_found(self):
        # given
        level = 2

        nodes = [
            (1, dict(label="E", x=0.0, y=1.0, level=level)),
            (2, dict(label="E", x=0.0, y=0.0, level=level)),
            (3, dict(label="E", x=1.0, y=0.0, level=level)),
            (4, dict(label="E", x=0.0, y=0.5, level=level)),
            (5, dict(label="E", x=0.5, y=0.0, level=level)),
            (6, dict(label="E", x=0.5, y=0.5, level=level)),
            (7, dict(label="I", x=1 / 3, y=2 / 3, level=level)),
            (8, dict(label="E", x=2 / 3, y=0.0, level=level)),
            (9, dict(label="I", x=1 / 3, y=1 / 3, level=level)),
        ]
        edges = [
            (1, 4),
            (4, 2),
            (2, 5),
            (5, 3),
            (3, 6),
            (6, 1),  # boundary edges
            (1, 8),
            (2, 8),  # internal edges
            (1, 7),
            (2, 7),
            (3, 7),  # internal I node of triangle <1,2,3>
            (1, 9),
            (2, 9),
            (8, 9),  # internal I node of triangle <1,2,8>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p5(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes) + 10)
        self.assertEqual(len(G.edges), len(edges) + 25)
        self.assertEqual(G.nodes[7]["label"], "i")
        self.assertEqual(G.nodes[9]["label"], "I")

    def test_should_not_split_when_constraints_not_met(self):
        # given
        level = 2

        nodes = [
            (1, dict(label="E", x=0.0, y=1.0, level=level)),
            (2, dict(label="E", x=0.0, y=0.0, level=level)),
            (3, dict(label="E", x=1.0, y=0.0, level=level)),
            (4, dict(label="E", x=0.0, y=0.5, level=level)),
            (5, dict(label="E", x=0.4, y=0.0, level=level)),
            (6, dict(label="E", x=0.5, y=0.5, level=level)),
            (7, dict(label="I", x=1 / 3, y=2 / 3, level=level)),
            (8, dict(label="E", x=2 / 3, y=0.0, level=level)),
            (9, dict(label="I", x=1 / 3, y=1 / 3, level=level)),
        ]
        edges = [
            (1, 4),
            (4, 2),
            (2, 5),
            (5, 3),
            (3, 6),
            (6, 1),  # boundary edges
            (1, 8),
            (2, 8),  # internal edges
            (1, 7),
            (2, 7),
            (3, 7),  # internal I node of triangle <1,2,3>
            (1, 9),
            (2, 9),
            (8, 9),  # internal I node of triangle <1,2,8>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p5(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))
        self.assertEqual(G.nodes[7]["label"], "I")
        self.assertEqual(G.nodes[9]["label"], "I")

    def test_should_not_split_when_constraints_not_met_deleted_node(self):
        # given
        level = 2

        nodes = [
            (1, dict(label="E", x=0.0, y=1.0, level=level)),
            (2, dict(label="E", x=0.0, y=0.0, level=level)),
            (3, dict(label="E", x=1.0, y=0.0, level=level)),
            (4, dict(label="E", x=0.0, y=0.5, level=level)),
            (6, dict(label="E", x=0.5, y=0.5, level=level)),
            (7, dict(label="I", x=1 / 3, y=2 / 3, level=level)),
            (8, dict(label="E", x=2 / 3, y=0.0, level=level)),
            (9, dict(label="I", x=1 / 3, y=1 / 3, level=level)),
        ]
        edges = [
            (1, 4),
            (4, 2),
            (2, 3),
            (3, 6),
            (6, 1),  # boundary edges
            (1, 8),
            (2, 8),  # internal edges
            (1, 7),
            (2, 7),
            (3, 7),  # internal I node of triangle <1,2,3>
            (1, 9),
            (2, 9),
            (8, 9),  # internal I node of triangle <1,2,8>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p5(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))
        self.assertEqual(G.nodes[7]["label"], "I")
        self.assertEqual(G.nodes[9]["label"], "I")

    def test_should_not_split_when_constraints_not_met_edge_deleted(self):
        # given
        level = 2

        nodes = [
            (1, dict(label="E", x=0.0, y=1.0, level=level)),
            (2, dict(label="E", x=0.0, y=0.0, level=level)),
            (3, dict(label="E", x=1.0, y=0.0, level=level)),
            (4, dict(label="E", x=0.0, y=0.5, level=level)),
            (6, dict(label="E", x=0.5, y=0.5, level=level)),
            (7, dict(label="I", x=1 / 3, y=2 / 3, level=level)),
            (8, dict(label="E", x=2 / 3, y=0.0, level=level)),
            (9, dict(label="I", x=1 / 3, y=1 / 3, level=level)),
        ]
        edges = [
            (1, 4),
            (4, 2),
            (3, 6),
            (6, 1),  # boundary edges
            (1, 8),
            (2, 8),  # internal edges
            (1, 7),
            (2, 7),
            (3, 7),  # internal I node of triangle <1,2,3>
            (1, 9),
            (2, 9),
            (8, 9),  # internal I node of triangle <1,2,8>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p5(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))
        self.assertEqual(G.nodes[7]["label"], "I")
        self.assertEqual(G.nodes[9]["label"], "I")

    def test_should_do_nothing_when_node_labels_dont_match(self):
        # given
        level = 2

        nodes = [
            (1, dict(label="E", x=0.0, y=1.0, level=level)),
            (2, dict(label="E", x=0.0, y=0.0, level=level)),
            (3, dict(label="E", x=1.0, y=0.0, level=level)),
            (4, dict(label="E", x=0.0, y=0.5, level=level)),
            (5, dict(label="I", x=0.5, y=0.0, level=level)),
            (6, dict(label="E", x=0.5, y=0.5, level=level)),
            (7, dict(label="E", x=1 / 3, y=2 / 3, level=level)),
            (8, dict(label="E", x=2 / 3, y=0.0, level=level)),
            (9, dict(label="I", x=1 / 3, y=1 / 3, level=level)),
        ]
        edges = [
            (1, 4),
            (4, 2),
            (2, 5),
            (5, 3),
            (3, 6),
            (6, 1),  # boundary edges
            (1, 8),
            (2, 8),  # internal edges
            (1, 7),
            (2, 7),
            (3, 7),  # internal I node of triangle <1,2,3>
            (1, 9),
            (2, 9),
            (8, 9),  # internal I node of triangle <1,2,8>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p5(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))


class P6_Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_should_do_nothing_when_no_isomorphic_subgraph_found(self):
        # given
        level = 2
        nodes = [
            (0, dict(label="i", x=0.5, y=0.5, level=level)),
            (1, dict(label="i", x=1.0, y=0.0, level=level)),
            (2, dict(label="E", x=0.0, y=0.0, level=level)),
            (3, dict(label="E", x=1.0, y=1.0, level=level)),
            (4, dict(label="I", x=1 / 3, y=1 / 3, level=level + 1)),
            (5, dict(label="I", x=2 / 3, y=2 / 3, level=level + 1)),
            (6, dict(label="E", x=0.0, y=0.0, level=level + 1)),
            (8, dict(label="E", x=1.0, y=1.0, level=level + 1)),
            (9, dict(label="I", x=1 / 3, y=1 / 3, level=level + 1)),
            (10, dict(label="I", x=2 / 3, y=2 / 3, level=level + 1)),
            (11, dict(label="E", x=0.0, y=0.0, level=level + 1)),
            (12, dict(label="E", x=0.5, y=0.5, level=level + 1)),
            (13, dict(label="E", x=1.0, y=1.0, level=level + 1)),
            (14, dict(label="E", x=2 / 3, y=2 / 3, level=level + 1)),
            (15, dict(label="E", x=1.0, y=2 / 3, level=level + 1)),
            (16, dict(label="E", x=1 / 3, y=1.0, level=level + 1)),
        ]

        edges = [
            (0, 2),
            (0, 3),
            (1, 2),
            (1, 3),
            (0, 4),
            (0, 5),
            (1, 9),
            (1, 10),
            (4, 6),
            (5, 8),
            (6, 8),
            (9, 11),
            (9, 12),
            (10, 12),
            (10, 13),
            (11, 12),
            (12, 13),
            (13, 14),
            (14, 15),
            (15, 16),
            (16, 14),
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p6(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))

    def test_should_merge_nodes_when_isomorphic_subgraph_found(self):
        # given
        level = 2
        nodes = [
            (0, dict(label="i", x=0.5, y=0.5, level=level)),
            (1, dict(label="i", x=1.0, y=0.0, level=level)),
            (2, dict(label="E", x=0.0, y=0.0, level=level)),
            (3, dict(label="E", x=1.0, y=1.0, level=level)),
            (4, dict(label="I", x=1 / 3, y=1 / 3, level=level + 1)),
            (5, dict(label="I", x=2 / 3, y=2 / 3, level=level + 1)),
            (6, dict(label="E", x=0.0, y=0.0, level=level + 1)),
            (7, dict(label="E", x=0.5, y=0.5, level=level + 1)),
            (8, dict(label="E", x=1.0, y=1.0, level=level + 1)),
            (9, dict(label="I", x=1 / 3, y=1 / 3, level=level + 1)),
            (10, dict(label="I", x=2 / 3, y=2 / 3, level=level + 1)),
            (11, dict(label="E", x=0.0, y=0.0, level=level + 1)),
            (12, dict(label="E", x=0.5, y=0.5, level=level + 1)),
            (13, dict(label="E", x=1.0, y=1.0, level=level + 1)),
            (14, dict(label="E", x=2 / 3, y=2 / 3, level=level + 1)),
            (15, dict(label="E", x=1.0, y=2 / 3, level=level + 1)),
            (16, dict(label="E", x=1 / 3, y=1.0, level=level + 1)),
        ]

        edges = [
            (0, 2),
            (0, 3),
            (1, 2),
            (1, 3),
            (0, 4),
            (0, 5),
            (1, 9),
            (1, 10),
            (4, 6),
            (4, 7),
            (5, 7),
            (5, 8),
            (6, 7),
            (7, 8),
            (9, 11),
            (9, 12),
            (10, 12),
            (10, 13),
            (11, 12),
            (12, 13),
            (13, 14),
            (14, 15),
            (15, 16),
            (16, 14),
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p6(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes) - 3)
        self.assertEqual(len(G.edges), len(edges) - 2)

    def test_should_do_nothing_when_middle_node_constraint_not_met(self):
        # given
        level = 2
        nodes = [
            (0, dict(label="i", x=0.5, y=0.5, level=level)),
            (1, dict(label="i", x=1.0, y=0.0, level=level)),
            (2, dict(label="E", x=0.0, y=0.0, level=level)),
            (3, dict(label="E", x=1.0, y=1.0, level=level)),
            (4, dict(label="I", x=1 / 3, y=1 / 3, level=level + 1)),
            (5, dict(label="I", x=2 / 3, y=2 / 3, level=level + 1)),
            (6, dict(label="E", x=0.0, y=0.0, level=level + 1)),
            (7, dict(label="E", x=0.6, y=0.5, level=level + 1)),
            (8, dict(label="E", x=1.0, y=1.0, level=level + 1)),
            (9, dict(label="I", x=1 / 3, y=1 / 3, level=level + 1)),
            (10, dict(label="I", x=2 / 3, y=2 / 3, level=level + 1)),
            (11, dict(label="E", x=0.0, y=0.0, level=level + 1)),
            (12, dict(label="E", x=0.5, y=0.5, level=level + 1)),
            (13, dict(label="E", x=1.0, y=1.0, level=level + 1)),
            (14, dict(label="E", x=2 / 3, y=2 / 3, level=level + 1)),
            (15, dict(label="E", x=1.0, y=2 / 3, level=level + 1)),
            (16, dict(label="E", x=1 / 3, y=1.0, level=level + 1)),
        ]

        edges = [
            (0, 2),
            (0, 3),
            (1, 2),
            (1, 3),
            (0, 4),
            (0, 5),
            (1, 9),
            (1, 10),
            (4, 6),
            (4, 7),
            (5, 7),
            (5, 8),
            (6, 7),
            (7, 8),
            (9, 11),
            (9, 12),
            (10, 12),
            (10, 13),
            (11, 12),
            (12, 13),
            (13, 14),
            (14, 15),
            (15, 16),
            (16, 14),
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p6(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))

    def test_should_do_nothing_when_equal_nodes_constraint_not_met(self):
        # given
        level = 2
        nodes = [
            (0, dict(label="i", x=0.5, y=0.5, level=level)),
            (1, dict(label="i", x=1.0, y=0.0, level=level)),
            (2, dict(label="E", x=0.0, y=0.0, level=level)),
            (3, dict(label="E", x=1.0, y=1.0, level=level)),
            (4, dict(label="I", x=1 / 3, y=1 / 3, level=level + 1)),
            (5, dict(label="I", x=2 / 3, y=2 / 3, level=level + 1)),
            (6, dict(label="E", x=0.0, y=0.0, level=level + 1)),
            (7, dict(label="E", x=0.5, y=0.5, level=level + 1)),
            (8, dict(label="E", x=1.0, y=1.0, level=level + 1)),
            (9, dict(label="I", x=1 / 3, y=1 / 3, level=level + 1)),
            (10, dict(label="I", x=2 / 3, y=2 / 3, level=level + 1)),
            (11, dict(label="E", x=0.2, y=0.0, level=level + 1)),
            (12, dict(label="E", x=0.5, y=0.5, level=level + 1)),
            (13, dict(label="E", x=1.0, y=1.0, level=level + 1)),
            (14, dict(label="E", x=2 / 3, y=2 / 3, level=level + 1)),
            (15, dict(label="E", x=1.0, y=2 / 3, level=level + 1)),
            (16, dict(label="E", x=1 / 3, y=1.0, level=level + 1)),
        ]

        edges = [
            (0, 2),
            (0, 3),
            (1, 2),
            (1, 3),
            (0, 4),
            (0, 5),
            (1, 9),
            (1, 10),
            (4, 6),
            (4, 7),
            (5, 7),
            (5, 8),
            (6, 7),
            (7, 8),
            (9, 11),
            (9, 12),
            (10, 12),
            (10, 13),
            (11, 12),
            (12, 13),
            (13, 14),
            (14, 15),
            (15, 16),
            (16, 14),
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p6(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))

    def test_should_merge_nodes_when_node_labels_dont_match(self):
        # given
        level = 2
        nodes = [
            (0, dict(label="i", x=0.5, y=0.5, level=level)),
            (1, dict(label="i", x=1.0, y=0.0, level=level)),
            (2, dict(label="E", x=0.0, y=0.0, level=level)),
            (3, dict(label="E", x=1.0, y=1.0, level=level)),
            (4, dict(label="I", x=1 / 3, y=1 / 3, level=level + 1)),
            (5, dict(label="I", x=2 / 3, y=2 / 3, level=level + 1)),
            (6, dict(label="E", x=0.0, y=0.0, level=level + 1)),
            (7, dict(label="E", x=0.5, y=0.5, level=level + 1)),
            (8, dict(label="I", x=1.0, y=1.0, level=level + 1)),
            (9, dict(label="E", x=1 / 3, y=1 / 3, level=level + 1)),
            (10, dict(label="I", x=2 / 3, y=2 / 3, level=level + 1)),
            (11, dict(label="E", x=0.0, y=0.0, level=level + 1)),
            (12, dict(label="E", x=0.5, y=0.5, level=level + 1)),
            (13, dict(label="E", x=1.0, y=1.0, level=level + 1)),
            (14, dict(label="E", x=2 / 3, y=2 / 3, level=level + 1)),
            (15, dict(label="E", x=1.0, y=2 / 3, level=level + 1)),
            (16, dict(label="E", x=1 / 3, y=1.0, level=level + 1)),
        ]

        edges = [
            (0, 2),
            (0, 3),
            (1, 2),
            (1, 3),
            (0, 4),
            (0, 5),
            (1, 9),
            (1, 10),
            (4, 6),
            (4, 7),
            (5, 7),
            (5, 8),
            (6, 7),
            (7, 8),
            (9, 11),
            (9, 12),
            (10, 12),
            (10, 13),
            (11, 12),
            (12, 13),
            (13, 14),
            (14, 15),
            (15, 16),
            (16, 14),
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p6(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))


class P9_Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_should_do_nothing_when_no_isomorphic_subgraph_found(self):
        # given
        level = 2

        nodes = [
            (1, dict(label="E", x=0.0, y=1.0, level=level)),
            (2, dict(label="E", x=1.0, y=1.0, level=level)),
            (3, dict(label="E", x=1.0, y=0.0, level=level)),
            (4, dict(label="E", x=0.0, y=0.0, level=level)),
            (5, dict(label="I", x=1 / 3, y=2 / 3, level=level)),
            (6, dict(label="I", x=2 / 3, y=1 / 3, level=level)),
        ]
        edges = [
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 1),  # boundary edges
            (2, 4),  # internal edge
            (1, 5),
            (2, 5),  # (4,5), # internal I node of triangle <1,2,4> with missing edge
            (2, 6),
            (3, 6),  # (4,6)  # internal I node of triangle <2,3,4> with missing edge
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p9(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))
        self.assertEqual(G.nodes[5]["label"], "I")
        self.assertEqual(G.nodes[6]["label"], "I")

    def test_should_split_trianle_when_isomorphic_subgraph_found(self):
        # given
        level = 2

        nodes = [
            (1, dict(label="E", x=0.0, y=1.0, level=level)),
            (2, dict(label="E", x=1.0, y=1.0, level=level)),
            (3, dict(label="E", x=1.0, y=0.0, level=level)),
            (4, dict(label="E", x=0.0, y=0.0, level=level)),
            (5, dict(label="I", x=1 / 3, y=2 / 3, level=level)),
            (6, dict(label="I", x=2 / 3, y=1 / 3, level=level)),
        ]
        edges = [
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 1),  # boundary edges
            (2, 4),  # internal edge
            (1, 5),
            (2, 5),
            (4, 5),  # internal I node of triangle <1,2,4>
            (2, 6),
            (3, 6),
            (4, 6),  # internal I node of triangle <2,3,4>
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
            (1, dict(label="E", x=0.0, y=1.0, level=level)),
            (2, dict(label="E", x=1.0, y=1.0, level=level)),
            (3, dict(label="E", x=1.0, y=0.0, level=level)),
            (4, dict(label="E", x=0.0, y=0.0, level=level)),
            (5, dict(label="E", x=1 / 3, y=2 / 3, level=level)),
            (6, dict(label="E", x=2 / 3, y=1 / 3, level=level)),
        ]
        edges = [
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 1),  # boundary edges
            (2, 4),  # internal edge
            (1, 5),
            (2, 5),
            (4, 5),  # internal I node of triangle <1,2,4>
            (2, 6),
            (3, 6),
            (4, 6),  # internal I node of triangle <2,3,4>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p9(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))
        self.assertEqual(G.nodes[5]["label"], "E")
        self.assertEqual(G.nodes[6]["label"], "E")

    def test_should_do_nothing_when_extra_nodes_found(self):
        # given
        level = 2

        nodes = [
            (1, dict(label="E", x=0.0, y=1.0, level=level)),
            (2, dict(label="E", x=1.0, y=1.0, level=level)),
            (3, dict(label="E", x=0.0, y=0.0, level=level)),
            (4, dict(label="I", x=1 / 3, y=2 / 3, level=level)),
            (5, dict(label="E", x=1 / 2, y=1 / 2, level=level)),
        ]
        edges = [
            (1, 2),
            (2, 5),
            (5, 3),
            (3, 1),  # boundary edges
            (1, 4),
            (2, 4),
            (3, 4),  # internal I node of triangle <1,2,3>
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # when
        p9(G, level)

        # then
        self.assertEqual(len(G.nodes), len(nodes))
        self.assertEqual(len(G.edges), len(edges))
        self.assertEqual(G.nodes[4]["label"], "I")
        self.assertEqual(G.nodes[5]["label"], "E")


class P10_Test(unittest.TestCase):
    def setUp(self):
        pass

    def _idealGraph(self):
        nodes = [
            (0, dict(label="i", x=0, y=0, level=0)),
            (1, dict(label="i", x=1, y=1, level=0)),
            (2, dict(label="E", x=1, y=0, level=0)),
            (3, dict(label="E", x=0, y=1, level=0)),
            (4, dict(label="I", x=1, y=0, level=1)),
            (5, dict(label="I", x=1, y=0, level=1)),
            (6, dict(label="I", x=1, y=1, level=1)),
            (7, dict(label="E", x=1, y=0, level=1)),
            (8, dict(label="E", x=1 / 2, y=1 / 2, level=1)),
            (9, dict(label="E", x=0, y=1, level=1)),
            (10, dict(label="E", x=1, y=0, level=1)),
            (11, dict(label="E", x=0, y=1, level=1)),
        ]

        edges = [
            (0, 2),
            (0, 3),
            (1, 2),
            (1, 3),
            (2, 3),
            (0, 4),
            (0, 5),
            (1, 6),
            (4, 7),
            (4, 8),
            (5, 8),
            (5, 9),
            (6, 10),
            (6, 11),
            (7, 8),
            (8, 9),
            (10, 11),
        ]

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        return G

    def test_should_merge_nodes_when_isomorphic_subgraph_found(self):
        # given
        level = 0
        G = self._idealGraph()
        nodes_len = len(G.nodes)
        edge_len = len(G.edges)

        # when
        p10(G, level)

        # then
        self.assertEqual(len(G.nodes), nodes_len - 2)
        self.assertEqual(len(G.edges), edge_len - 1)

    def test_should_not_merge_nodes_when_isomorphic_subgraph_not_found(self):
        # given
        level = 0
        G = self._idealGraph()
        edge = next(iter(G.edges))
        G.remove_edge(edge[0], edge[1])
        nodes_len = len(G.nodes)
        edge_len = len(G.edges)

        # when
        p10(G, level)

        # then
        self.assertEqual(len(G.nodes), nodes_len)
        self.assertEqual(len(G.edges), edge_len)


if __name__ == "__main__":
    unittest.main()
