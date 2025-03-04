import re

# usage: python3 calculate_ddG_rosetta-parameters.py

# Define a function to extract the parameters and their values into a dictionary
def extract_values(row):
    # Updated pattern to match parameters with any number of spaces before the value
    pattern = r"(\S+):\s*(-?\d+\.\d+)"
    matches = re.findall(pattern, row)
    return {param: float(value) for param, value in matches}

# Read the contents from the file
def process_file(filename, output_filename="final_ddG_score.txt"):
    try:
        with open(filename, 'r') as file:
            # Read lines from the file
            lines = file.readlines()
            
            if len(lines) < 2:
                print("The file must contain at least two rows.")
                return
            
            # Extract values from the two rows
            row1_values = extract_values(lines[0])
            row2_values = extract_values(lines[1])
            
            # Calculate the differences between the two rows (row2 (MUT) - row1 (WT))
            differences = {}
            for param in row1_values:
                if param in row2_values:
                    difference = row2_values[param] - row1_values[param]  # Subtract row2 from row1
                    differences[param] = difference
            
            # Sort the differences from lowest to highest
            sorted_differences = sorted(differences.items(), key=lambda x: x[1])

            # Write the sorted differences to a file
            with open(output_filename, 'w') as output_file:
                for param, diff in sorted_differences:
                    output_file.write(f"{param}: {diff:.3f}\n")

            print(f"Results have been written to {output_filename}")
                
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    filename = 'mutation_list.ddg'  # Replace this with your ddg file name if different
    process_file(filename)
