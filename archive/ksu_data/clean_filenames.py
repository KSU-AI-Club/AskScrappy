import os
import re

# Directory containing your PDF files
directory = 'path_to_your_directory'

# Function to clean up file names
def clean_filename(filename):
    # Remove file extension to work with the base name
    base_name, extension = os.path.splitext(filename)
    
    # Remove leading numbers (e.g., 1.0, 2.0, etc.)
    base_name = re.sub(r'^\d+\.\d+\s*', '', base_name)
    
    # Replace spaces with underscores
    base_name = base_name.replace(' ', '_')
    
    # Remove periods (except the file extension)
    base_name = base_name.replace('.', '')
    
    # Remove commas
    base_name = base_name.replace(',', '')
    
    # Remove colons
    base_name = base_name.replace(':', '')
    
    # Replace ampersand with 'and'
    base_name = base_name.replace('&', 'and')
    
    # Remove question marks
    base_name = base_name.replace('?', '')
    
    # Add the extension back
    return base_name + extension

# Loop through each file in the directory and rename it
for filename in os.listdir(directory):
    if filename.endswith(".pdf"):
        new_name = clean_filename(filename)
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_name)
        
        # Rename the file
        os.rename(old_path, new_path)
        print(f'Renamed: {filename} -> {new_name}')

print("Renaming process completed.")

