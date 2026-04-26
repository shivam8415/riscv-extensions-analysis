import json
import os
from collections import defaultdict


def load_data(path):
    with open(path, "r") as f:
        return json.load(f)


def process_data(data):
    ext_map = defaultdict(list)
    multi_ext = []

    for mnemonic, details in data.items():
        extensions = details.get("extension", [])

        if len(extensions) > 1:
            multi_ext.append((mnemonic, extensions))

        for ext in extensions:
            ext_map[ext].append(mnemonic)

    return ext_map, multi_ext


def print_summary(ext_map):
    print("\n=== RISC-V Extension Summary ===\n")

    print(f"{'Extension':<18} | {'Count':<5} | Example")
    print("=" * 45)

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
    base_dir = os.path.dirname(os.path.abspath(__file__))

    possible_paths = [
        # when running from Task-1/
        os.path.join(base_dir, "riscv-extensions-landscape", "src", "instr_dict.json"),

        # when running from inside riscv-extensions-landscape/
        os.path.join(base_dir, "src", "instr_dict.json"),

        # fallback (if structure slightly different)
        os.path.join(base_dir, "..", "Task-1", "riscv-extensions-landscape", "src", "instr_dict.json"),
    ]

    json_path = None
    for path in possible_paths:
        if os.path.exists(path):
            json_path = path
            break

    if not json_path:
        print("❌ instr_dict.json not found in expected locations")
        for p in possible_paths:
            print("Checked:", p)
        return

    print("Using file:", json_path)  # debug (can remove later)

    data = load_data(json_path)

    ext_map, multi_ext = process_data(data)

    print_summary(ext_map)
    print_multi_ext(multi_ext)
    
if __name__ == "__main__":
    main()