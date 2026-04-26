# Task 1 – Instruction Parsing and Grouping

## Approach
- Parsed the JSON instruction file
- Extracted extension tags for each instruction
- Grouped instructions by their extension
- Counted instructions per extension
- Selected one example mnemonic per group

## Multi-extension Handling
- Identified instructions belonging to more than one extension
- Listed them separately

## Output
- Displayed a formatted table showing:
  - Extension
  - Instruction count
  - Example mnemonic

## Notes
- Handled missing or empty extension fields safely
- Sorted extensions by instruction count for better readability