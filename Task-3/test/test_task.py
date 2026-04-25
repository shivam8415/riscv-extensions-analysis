import unittest
from collections import defaultdict
from itertools import combinations


# -------- NORMALIZE --------
def normalize_json_ext(ext):
    ext = ext.lower()
    return ext.replace("rv32_", "").replace("rv64_", "").replace("rv_", "")


# -------- BUILDING GRAPH --------
def build_graph(data):
    graph = defaultdict(set)

    for mnemonic, details in data.items():
        extensions = details.get("extension") or []
        extensions = [normalize_json_ext(e) for e in extensions]

        # connecting extensions that share instruction
        for a, b in combinations(extensions, 2):
            graph[a].add(b)
            graph[b].add(a)

    return graph


# -------- TEST CLASS --------
class TestFunctions(unittest.TestCase):

    def test_normalization(self):
        self.assertEqual(normalize_json_ext("rv64_zba"), "zba")
        self.assertEqual(normalize_json_ext("rv_i"), "i")

    def test_multiple_cases(self):
        self.assertEqual(normalize_json_ext("rv32_zbb"), "zbb")
        self.assertEqual(normalize_json_ext("rv64_m"), "m")

    def test_graph_connections(self):
        data = {
            "inst1": {"extension": ["rv64_zba", "rv64_zbb"]},
            "inst2": {"extension": ["rv64_zbb", "rv64_zbc"]}
        }

        graph = build_graph(data)

        # zba should connect to zbb
        self.assertIn("zbb", graph["zba"])

        # zbb should connect to zbc
        self.assertIn("zbc", graph["zbb"])

        # zba should NOT connect directly to zbc
        self.assertNotIn("zbc", graph["zba"])



if __name__ == "__main__":
    unittest.main()