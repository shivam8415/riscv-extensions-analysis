import json
import os
import re


# -------- LOADING JSON --------
def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


# -------- NORMALIZE JSON EXTENSIONS --------
def normalize_json_ext(ext):
    ext = ext.lower()
    ext = ext.replace("rv32_", "").replace("rv64_", "").replace("rv_", "")
    return ext


# -------- GETTING EXTENSIONS FROM JSON --------
def get_json_extensions(data):
    exts = set()

    for details in data.values():
        for ext in details.get("extension") or []:
            exts.add(normalize_json_ext(ext))

    return exts


# -------- CLEAN MANUAL EXTENSIONS --------
VALID_SINGLE = {"i", "m", "a", "f", "d", "q"}

def clean_manual_ext(ext):
    ext = ext.lower()

    # Keep base extensions
    if ext in VALID_SINGLE:
        return ext

    # Keeping meaningful Z extensions
    if ext.startswith("z"):
        # removing short junk like "za"
        if len(ext) < 3:
            return None

        # filtering obvious English words
        if ext.startswith(("zero", "zhang")):
            return None

        return ext

    return None


# -------- EXTRACTING EXTENSIONS FROM ISA MANUAL --------
def extract_manual_extensions(folder):
    pattern = re.compile(r'\b(Z[a-z]{2,}[0-9]*|[IMAFDQ])\b', re.IGNORECASE)
    found = set()

    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".adoc"):
                path = os.path.join(root, file)

                try:
                    with open(path, "r", encoding="utf-8") as f:
                        text = f.read()
                        matches = pattern.findall(text)

                        for m in matches:
                            cleaned = clean_manual_ext(m)
                            if cleaned:
                                found.add(cleaned)

                except:
                    pass  

    return found



def main():
    json_path = "../Task-1/riscv-extensions-landscape/src/instr_dict.json"
    manual_path = "riscv-isa-manual/src"

    data = load_json(json_path)

    json_exts = get_json_extensions(data)
    manual_exts = extract_manual_extensions(manual_path)

    matched = json_exts & manual_exts
    json_only = json_exts - manual_exts
    manual_only = manual_exts - json_exts

    print("\n=== Cross Reference Report ===\n")

    print(f"Matched: {len(matched)}")
    print(f"Only in JSON: {len(json_only)}")
    print(f"Only in Manual: {len(manual_only)}")

    print("\n--- JSON Only ---")
    if not json_only:
        print("✔ None")
    else:
        for ext in sorted(json_only):
            print(ext)

    print("\n--- Manual Only ---")
    if not manual_only:
        print("✔ None")
    else:
        for ext in sorted(manual_only):
            print(ext)



if __name__ == "__main__":
    main()