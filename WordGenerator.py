import os
from openai import OpenAI
import time
import json

def generate_text(client, character_count):
    prompt = f"Explain the theory of gravity. The explanation should contain no formulas and be exactly {character_count} characters long."
    generated_text = ""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4o",
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
max_tries = 1
while tries < max_tries:    
    for target_character_count in range(5000, 10000, 500):
        if target_character_count in lookup_table:
            continue

        generated_text = generate_text(client, target_character_count)
        generated_text = generated_text.replace("\n\n", " ")
        character_count = len(generated_text)
        
        if character_count not in lookup_table:
            print(f"Generated text with {character_count} characters: {generated_text}")
            lookup_table[character_count] = generated_text
        else:
            print(f"Skipping duplicate entry with {character_count} characters")
    
    tries += 1

# Sort the lookup table by character count before saving
sorted_lookup_table = dict(sorted(lookup_table.items()))

# Save the updated lookup table to the JSON file
with open(lookup_table_path, "w") as file:
    json.dump(sorted_lookup_table, file, indent=4)