import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize

# Mapping of three-letter amino acid codes to one-letter codes
amino_acid_dict = {
    "ALA": "A", "CYS": "C", "ASP": "D", "GLU": "E", "PHE": "F", "GLY": "G", "HIS": "H", "ILE": "I",
    "LYS": "K", "LEU": "L", "MET": "M", "ASN": "N", "PRO": "P", "GLN": "Q", "ARG": "R", "SER": "S",
    "THR": "T", "VAL": "V", "TRP": "W", "TYR": "Y"
}

# Define the new mapping for the x-axis position labels
position_mapping = {
    "A201": "P201", "A202": "E202", "A203": "W203", "A204": "L204", "A205": "R205", "A206": "I206",
    "A207": "W207", "A208": "T208", "A209": "G209"
}

# Function to extract the total score from a .sc file
def extract_total_score(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()  # Read all lines in the file
        for i, line in enumerate(lines):
            if line.startswith("SCORE:"):
                # The total score is on the next line, so we get lines[i + 1]
                score_line = lines[i + 1].split()
                total_score = score_line[1]  # Grab the value from the second column (index 1)
                return float(total_score)
    return None

# Function to generate a heatmap from .sc files
def create_heatmap_from_sc_files():
    current_directory = os.getcwd()  # Get the current working directory
    mutants = []  # List to store mutant amino acids
    scores = []   # List to store corresponding total scores
    positions = []  # List to store wild-type positions
    mutant_aa_set = set()  # Set to store unique mutant amino acids
    positions_set = set()  # Set to store unique wild-type positions
    
    reference_values = {}  # Dictionary to store the reference value for each position
    
    # Define the reference files based on the provided mapping
    reference_files = {
        "A201": "A201_PROscore.sc",
        "A202": "A202_GLUscore.sc",
        "A203": "A203_TRPscore.sc",
        "A204": "A204_LEUscore.sc",
        "A205": "A205_ARGscore.sc",
        "A206": "A206_ILEscore.sc",
        "A207": "A207_TRPscore.sc",
        "A208": "A208_THRscore.sc",
        "A209": "A209_GLYscore.sc"
    }
    
    # Loop through files in the current directory
    for filename in os.listdir(current_directory):
        if '.sc' in filename:
            # Extract the mutant amino acid and position from the filename
            parts = filename.split('_')
            position = parts[0]  # Extract position
            mutant_aa = parts[1]  # Extract mutant amino acid like "GLN"
            
            # Remove the "score.sc" part if it exists in the mutant name
            mutant_aa_clean = mutant_aa.replace("score.sc", "")
            
            # Extract total score from the file
            total_score = extract_total_score(os.path.join(current_directory, filename))
            if total_score is not None:
                mutants.append(mutant_aa_clean)
                scores.append(total_score)
                positions.append(position)
                mutant_aa_set.add(mutant_aa_clean)
                positions_set.add(position)
                
                # Identify reference values based on predefined reference files
                if position in reference_files:
                    reference_value = extract_total_score(os.path.join(current_directory, reference_files[position]))
                    if reference_value is not None:
                        reference_values[position] = reference_value

    # Sort positions and mutants
    sorted_positions = sorted(positions_set)
    sorted_mutants = sorted(mutant_aa_set)

    # Create a matrix to store the scores (relative to the reference values)
    heatmap_matrix = np.zeros((len(sorted_mutants), len(sorted_positions)))  # Rows for mutants, columns for positions
    
    # For each mutant and position, compute the score difference relative to the reference
    for i, mutant in enumerate(sorted_mutants):
        for j, position in enumerate(sorted_positions):
            reference_value = reference_values.get(position, None)
            if reference_value is not None:
                # For each mutant and position, find the corresponding scores
                matching_scores = [scores[k] for k in range(len(mutants)) if mutants[k] == mutant and positions[k] == position]
                if matching_scores:
                    heatmap_matrix[i, j] = np.mean(matching_scores) - reference_value  # Store the score difference relative to the reference

    # Define the custom colors:
    colors = ['#008000', 'white', '#67001F']  # Red to white to blue
    cmap = LinearSegmentedColormap.from_list('CustomRedWhiteBlue', colors, N=256)

    # Normalize the color scale
    norm = Normalize(vmin=-6, vmax=6)
    
    # Update positions to use the new labels from the mapping
    updated_positions = [position_mapping.get(position, position) for position in sorted_positions]

    # Plotting the heatmap with flipped axes
    plt.figure(figsize=(10, 8))
    ax = sns.heatmap(heatmap_matrix, annot=True, fmt='.1f', xticklabels=updated_positions, yticklabels=sorted_mutants,
                     cmap=cmap, norm=norm, cbar=True, linewidths=0.25, linecolor='white')  # Add outline with white color

    # Set horizontal y-axis labels
    plt.yticks(rotation=0)  # This makes the y-axis labels horizontal
    plt.xlabel("Wild-Type Residues")
    plt.ylabel("Mutant Amino Acids")

    # Modify the colorbar label and rotate it by 270 degrees
    cbar = ax.collections[0].colorbar
    cbar.set_label("ΔE (REU)", fontsize=12, rotation=270)

    # Custom annotations: replace 0 with "WT"
    for text in ax.texts:
        if text.get_text() == '0.0':
            text.set_text('WT')

    # Save the heatmap as both PDF and PNG with the specified prefix
    plt.savefig("PointMutagenesisScan_Heatmap.pdf", format='pdf')
    plt.savefig("PointMutagenesisScan_Heatmap.png", format='png')

    # Display the plot
    plt.show()

# Run the function to create the heatmap
create_heatmap_from_sc_files()
