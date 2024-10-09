import os
from openai import OpenAI
import time
import json

lookup_table_range_from = 1 # Minimum character count to generate
lookup_table_range_to = 5000 # Maximum character count to generate
lookup_table_range_step = 50 # Step size for character count. Vary this in smaller ranges to fill the lookup table faster for smaller character counts
max_attempts = 1 # Number of attempts to generate text with specified character count

def get_promt(character_count):
    return f"Explain the theory of gravity. The explanation should contain no formulas and be exactly {character_count} characters long."

def generate_text(client, character_count):
    prompt = get_promt(character_count)
    generated_text = ""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4o-mini",
            #max_tokens=length,  # Note: tokens are not the same as characters
            temperature=0.8,
        )

        generated_text = chat_completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error occurred: {e}")
        tries += 1
        time.sleep(5)  # Wait before retrying in case of an error
    
    return generated_text

# Load the OpenAI API key from a file
api_key_path = "api_key.txt"
with open(api_key_path, "r", encoding="utf-8") as file:
    api_key = file.read().strip()

# Initialize the OpenAI client with the loaded API key
client = OpenAI(
    api_key=api_key,
)

# Load existing entries in the lookup table from a JSON file if it exists
lookup_table_path = "lookup_table.json"
if os.path.exists(lookup_table_path):
    with open(lookup_table_path, "r", encoding="utf-8") as file:
        lookup_table = json.load(file)
        # Convert string keys to integers
        lookup_table = {int(k): v for k, v in lookup_table.items()}
else:
    lookup_table = {}

tries = 0
while tries < max_attempts:    
    for target_character_count in range(lookup_table_range_from, lookup_table_range_to, lookup_table_range_step):
        if target_character_count in lookup_table:
            continue

        generated_text = generate_text(client, target_character_count)
        generated_text = generated_text.replace("\n\n", " ")
        character_count = len(generated_text)
        
        if character_count not in lookup_table:
            print(f"Target: {target_character_count}, Generated text with {character_count} characters")
            lookup_table[character_count] = generated_text
        else:
            print(f"Target: {target_character_count}, Skipping duplicate entry with {character_count} characters")
    
    tries += 1

# Sort the lookup table by character count before saving
sorted_lookup_table = dict(sorted(lookup_table.items()))

# Save the updated lookup table to the JSON file
with open(lookup_table_path, "w") as file:
    json.dump(sorted_lookup_table, file, indent=4)
    print(f"Lookup table saved to {lookup_table_path}")

# Check occupancy of the lookup table
lookup_table_size = len(lookup_table)
available_keys = len([key for key in range(lookup_table_range_from, lookup_table_range_to) if key in lookup_table])
percentage = (available_keys / (lookup_table_range_to - lookup_table_range_from)) * 100
print(f"Lookup table occupancy between {lookup_table_range_from} to {lookup_table_range_to}: {percentage:.1f}%")

# Visualize the lookup table occupancy
import matplotlib.pyplot as plt

# Extracting the keys from the dictionary
keys = sorted(lookup_table.keys())

# Create a plot
plt.figure(figsize=(10, 2))

# Plot the keys on a number line as dots
plt.scatter(keys, [1] * len(keys), marker="|", color="blue", s=200)

# Formatting the plot
plt.title("Lookup Table")
plt.xlabel("Characters")
plt.yticks([])  # Remove the y-axis as it is not needed
plt.grid(True, axis='x', linestyle='--', alpha=0.7)

# Show the plot
plt.tight_layout()
plt.show()