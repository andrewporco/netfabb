# Function to read the text file, process it, and write the output to a new file
def process_text_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        text = file.read()
    
    # Split the text into words
    words = text.split()
    
    # Add quotes and comma around each word
    modified_words = [f'"{word}",' for word in words]
    
    # Join the modified words back into a single string
    modified_text = ' '.join(modified_words)
    
    # Write the modified text to the output file
    with open(output_file_path, 'w') as file:
        file.write(modified_text)

# Define the input and output file paths
input_file_path = r"C:\Users\XuanLiang\Desktop\filenames.txt"  # Replace with your input file path
output_file_path = r"C:\Users\XuanLiang\Desktop\output.txt" # Replace with your desired output file path

# Process the text file
process_text_file(input_file_path, output_file_path)
