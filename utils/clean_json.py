import re
import json

# Input data as a string (to handle comments)
with open('data/weaponcategories.jsonc') as f:
    raw_data = f.read()
# Clean and parse the data
def parse_json_with_comments(raw_data):
    cleaned_data = {}
    # Use regex to match key-value-comment pattern
    #matches = re.findall(r'"(\w+)":\s*\d+,\s*//(.+)', raw_data)
    matches = re.findall(r'"(\w+)",\s*//(.+)', raw_data)
    for key, name in matches:
        cleaned_data[key] = name.strip()
    return cleaned_data

# Process the raw data
formatted_data = parse_json_with_comments(raw_data)

# Save the cleaned data to a JSON file
with open("reformatted_data.json", "w") as json_file:
    json.dump(formatted_data, json_file, indent=4)

print("Reformatted JSON saved as 'reformatted_data.json'")
