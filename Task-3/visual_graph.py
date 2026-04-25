import json
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations


# -------- LOAD DATA --------
def load_data(path):
    with open(path, "r") as f:
        return json.load(f)


# -------- NORMALIZE --------
def normalize(ext):
    ext = ext.lower()
    return ext.replace("rv32_", "").replace("rv64_", "").replace("rv_", "")


# -------- BUILD GRAPH --------
def build_graph(data):
    G = nx.Graph()

    for mnemonic, details in data.items():
        extensions = details.get("extension") or []
        extensions = [normalize(e) for e in extensions]

        # add nodes
        for ext in extensions:
            G.add_node(ext)

        # connect nodes if instruction belongs to multiple extensions
        for a, b in combinations(extensions, 2):
            G.add_edge(a, b)

    return G


# -------- MAIN --------
def main():
    path = "../Task-1/riscv-extensions-landscape/src/instr_dict.json"

    data = load_data(path)
    G = build_graph(data)

    print(f"Total Nodes: {len(G.nodes())}")
    print(f"Total Edges: {len(G.edges())}")

    # ✅ REMOVE NOISE (isolated nodes)
    G.remove_nodes_from(list(nx.isolates(G)))

    print(f"After filtering → Nodes: {len(G.nodes())}, Edges: {len(G.edges())}")

    # ✅ BETTER LAYOUT
    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, k=0.4, seed=42)

    # ✅ NODE SIZE BASED ON CONNECTIONS (importance)
    node_sizes = [400 + 300 * G.degree(n) for n in G.nodes()]

    # ✅ DRAW GRAPH
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=node_sizes,
        node_color="skyblue",
        edge_color="gray",
        font_size=8,
        font_weight="bold"
    )
    
    plt.title("RISC-V Extension Relationship Graph (Filtered & Clean)")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()