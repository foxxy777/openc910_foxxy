import os

def combine_files_in_directory(output_file_name="combined_file.txt"):
    # Get the list of all files in the current directory
    files = [f for f in os.listdir() if os.path.isfile(f)]
    
    with open(output_file_name, 'w', encoding='utf-8') as output_file:
        for file_name in files:
            try:
                # Try to open each file and write its content to the output file
                with open(file_name, 'r', encoding='utf-8') as input_file:
                    content = input_file.read()
                    output_file.write(f"--- Start of {file_name} ---\n")
                    output_file.write(content)
                    output_file.write(f"\n--- End of {file_name} ---\n\n")
            except UnicodeDecodeError:
                # If there's a UnicodeDecodeError, try opening with 'latin-1' encoding
                with open(file_name, 'r', encoding='latin-1') as input_file:
                    content = input_file.read()
                    output_file.write(f"--- Start of {file_name} ---\n")
                    output_file.write(content)
                    output_file.write(f"\n--- End of {file_name} ---\n\n")
            except Exception as e:
                print(f"Error reading {file_name}: {e}")
    
    print(f"All files have been combined into {output_file_name}")

# Run the function to combine files
combine_files_in_directory()
