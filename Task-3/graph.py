import json
from itertools import combinations
from collections import defaultdict


# -------- LOAD DATA --------
def load_data(path):
    with open(path, "r") as f:
        return json.load(f)


# -------- NORMALIZE EXTENSIONS --------
def normalize(ext):
    ext = ext.lower()
    return ext.replace("rv32_", "").replace("rv64_", "").replace("rv_", "")


# -------- BUILD GRAPH --------
def build_graph(data):
    graph = defaultdict(set)

    for mnemonic, details in data.items():
        extensions = details.get("extension") or []
        extensions = [normalize(e) for e in extensions]

        for a, b in combinations(extensions, 2):
            graph[a].add(b)
            graph[b].add(a)

    return graph


# -------- PRINT GRAPH --------
def print_graph(graph):
    print("\n=== Extension Relationship Graph ===\n")

    for ext, neighbors in sorted(graph.items()):
        if neighbors:
            print(f"{ext:<10} → {', '.join(sorted(neighbors))}")


# -------- MAIN --------
def main():
    path = "../Task-1/riscv-extensions-landscape/src/instr_dict.json"

    data = load_data(path)
    graph = build_graph(data)

    print_graph(graph)


if __name__ == "__main__":
    main()