with open('docs/fika.log', 'r') as f:
    log_content = f.read()

# Split the log file into lines
lines = log_content.splitlines()

# Create a set to store unique URLs
unique_urls = set()

# Iterate through each line
for line in lines:
    # Check if the line starts with "[Client Request]"
    if line.startswith("[Client Request]"):
        # Extract the portion after "[Client Request]"
        url = line.split("]", 1)[-1].strip()
        # Remove IP address if present
        if "\\" in url:
            url = url.split("\\", 1)[1]
        elif "/" in url:
            url = url.split("/", 1)[1]
        # Ensure URLs are uniform (replace backslashes with forward slashes)
        url = url.replace("\\", "/")
        # Add the URL to the set if not empty
        if url:
            unique_urls.add(url)

# Define the output file path
output_file = "unique_urls.txt"

# Write the unique URLs to the file
with open(output_file, "w") as file:
    for url in sorted(unique_urls):
        file.write(url + "\n")
