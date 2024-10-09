import os
import json

# Load existing entries in the lookup table from a JSON file if it exists
lookup_table_path = "lookup_table.json"
if os.path.exists(lookup_table_path):
    with open(lookup_table_path, "r", encoding="utf-8") as file:
        lookup_table = json.load(file)
        # Convert string keys to integers
        lookup_table = {int(k): v for k, v in lookup_table.items()}
else:
    quit("Lookup table not found. Please run WordGenerator.py first to generate the lookup table.")

# Print the lookup table in the specified JavaScript format
output_file_path = "lookup_table.js"

with open(output_file_path, "w", encoding="utf-8") as file:
    file.write("var lookupTable = {\n")
    keys = sorted(lookup_table.keys())
    for i, key in enumerate(keys):
        value = lookup_table[key]
        # Escape double quotes and backslashes for JavaScript compatibility
        value = value.replace('\\', '\\\\').replace('"', '\\"')
        comma = "," if i < len(keys) - 1 else ""
        file.write(f"    {key}: \"{value}\"{comma}\n")
    file.write("};\n")

print(f"Lookup table saved to {output_file_path}")