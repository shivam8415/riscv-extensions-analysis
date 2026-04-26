import json
from collections import defaultdict


def load_data(path):
    with open(path, "r") as f:
        return json.load(f)


def process_data(data):
    ext_map = defaultdict(list)
    multi_ext = []

    for mnemonic, details in data.items():
        extensions = details.get("extension") or []

        if len(extensions) > 1:
            multi_ext.append((mnemonic, extensions))

        for ext in extensions:
            ext_map[ext].append(mnemonic)

    return ext_map, multi_ext


def print_summary(ext_map):
    print("\n=== RISC-V Extension Summary ===\n")

    print(f"{'Extension':<18} | {'Count':<5} | Example")
    print("=" * 45)

    # sorting
    sorted_ext = sorted(ext_map.items(), key=lambda x: len(x[1]), reverse=True)

    for ext, mnemonics in sorted_ext:
        count = len(mnemonics)
        example = mnemonics[0] if mnemonics else "N/A"
        print(f"{ext:<18} | {count:<5} | {example}")

    print("=" * 45)


def print_multi_ext(multi_ext):
    print("\n=== Multi-Extension Instructions ===\n")

    if not multi_ext:
        print("✔ None found")
    else:
        for mnemonic, exts in multi_ext:
            print(f"• {mnemonic:<12} → {', '.join(exts)}")


def main():
    data = load_data("src/instr_dict.json")

    ext_map, multi_ext = process_data(data)

    print_summary(ext_map)
    print_multi_ext(multi_ext)


if __name__ == "__main__":
    main()