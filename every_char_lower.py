import re
def lowercase_text_file(input_file, output_file, search_words):
    try:
        # Open the input file for reading
        with open(input_file, 'r') as file:
            # Read the content of the file
            for line_number, line in enumerate(file, start=1):
                # Check if any of the search words are present in the line
                for word in search_words:
                    if word.lower() in line.lower():
                        # pattern = re.compile(word.replace('*', '\\d*'), re.IGNORECASE)
                        print(f"Found '{word}' in line {line_number}: {line.strip()}")
        
#         # Convert the text to lowercase
#         lowercase_text = text.lower()
        
#         # Open the output file for writing
#         with open(output_file, 'w') as file:
#             # Write the lowercase text to the output file
#             file.write(lowercase_text)
        
#         print("Conversion complete. Lowercased text saved to", output_file)

    except FileNotFoundError:
        print("File not found. Please make sure the file path is correct.")

# # Example usage:
# input_file = "input.txt"  # Replace "input.txt" with your input file path
# output_file = "output.txt"  # Replace "output.txt" with your output file path

# lowercase_text_file("C:\\Users\\RikDeHoop\\sld_kvt_ts.txt", "sld_kvt_ts_lower.txt", ['Kazerne1'])
def replace_words_in_text(input_file, replacements):
    try:
        # Open the input file for reading
        with open(input_file, 'r') as file:
            # Read the content of the file
            text = file.read()

        # Iterate over the replacements
        for old_word, new_word in replacements.items():
            # Use regular expression to find and replace words, maintaining case
            text = re.sub(r'\b' + re.escape(old_word) + r'\b', new_word.lower(), text, flags=re.IGNORECASE)

        # Write the modified text back to the file
        with open(input_file, 'w') as file:
            file.write(text)

        print("Replacement complete. File updated:", input_file)

    except FileNotFoundError:
        print("File not found. Please make sure the file path is correct.")

# Example usage:
input_file = "C:\\Users\\RikDeHoop\\KVT_TS.txt"  # Replace "input.txt" with your input file path
replacements = {"Kazerne1": "kazerne1"}  # Add your replacements here

# replace_words_in_text(input_file, replacements)
db_params = {
    'dbtype': 'postgis',
    'host': 'geo.vrbn.nl',
    'port': '5432',
    'database': 'mapgallery',
    'user': 'geo',
    'passwd': 'iELo3Y9/OZDE'
}
print(f'postgresql://{db_params["user"]}:{db_params["passwd"]}@{db_params["host"]}:{db_params["port"]}/{db_params["database"]}')