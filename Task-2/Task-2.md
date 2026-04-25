# Task 2 – Cross-Referencing with RISC-V ISA Manual

## Approach

For this task, I worked with two data sources:
1. `instr_dict.json` (instruction dataset)
2. The official RISC-V ISA manual (AsciiDoc files)

First, I extracted all extension tags from the JSON file by iterating through each instruction and collecting its associated extensions. Since the JSON uses prefixes like `rv32_`, `rv64_`, and `rv_`, I normalized these to make comparison easier.

Next, I scanned the ISA manual source files located in the `src/` directory. I used a regex-based approach to extract extension names such as `Zba`, `Zicsr`, `M`, `F`, etc. Since the manual contains a lot of general text, I applied filtering to remove unrelated words and keep only valid extension-like patterns.

## Cross-Referencing

After collecting extensions from both sources, I normalized everything to lowercase and compared them using set operations:

- Found extensions present in both sources (matched)
- Identified extensions present only in the JSON dataset
- Identified extensions present only in the ISA manual

## Observations

- Several extensions matched successfully between the two sources.
- Some extensions appeared only in the JSON dataset. Many of these were:
  - Combined extensions (e.g., `zfh_zfa`, `d_zfa`)
  - Internal or tool-specific naming formats
- Some extensions appeared only in the ISA manual, indicating that:
  - They are not yet mapped in the dataset
  - Or naming differences prevented matching

## Challenges

- Extension naming conventions differ between sources (e.g., `rv_zba` vs `Zba`)
- The ISA manual contains general English words that can be mistakenly captured as extensions
- Some JSON entries combine multiple extensions into a single tag

## Conclusion

This task highlights inconsistencies between the instruction dataset and the ISA manual. The differences observed are expected and useful for improving coverage and alignment. The implemented approach successfully identifies these mismatches and provides a clear comparison summary.