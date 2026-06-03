import os
import numpy as np
import matplotlib.pyplot as plt

def read_xvg(filepath, col):
    """Parses a GROMACS .xvg file and extracts a specific column."""
    data = []
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as f:
        for line in f:
            if not line.startswith('@') and not line.startswith('#'):
                parts = line.split()
                if len(parts) > col:
                    data.append(float(parts[col]))
    return np.array(data)

# Define the paths for Replica 3 of all three molecules
files_to_plot = {
    'ETQ': '../../3PBL-ETQ/results/run3_gpu/rmsd_replica3.xvg',
    'MOD1': '../../3PBL-MOD/MOD1/results_repl3_MOD1/rmsd_repl3_MOD1.xvg',
    'MOD2': '../../3PBL-MOD/MOD2/results_repl3_MOD2/rmsd_repl3_MOD2.xvg'
}

# Use distinct colors for contrast
colors = {
    'ETQ': 'black', 
    'MOD1': 'blue', 
    'MOD2': 'red'
}

plt.figure(figsize=(12, 7))

for label, filepath in files_to_plot.items():
    rmsd_nm = read_xvg(filepath, 1)
    
    if rmsd_nm is None:
        print(f"Missing data for {label}. Please check the file path: {filepath}")
        continue
        
    # Convert nanometers to Angstroms
    rmsd_angstrom = rmsd_nm * 10.0
    
    # Generate an array of frame numbers
    frames = np.arange(len(rmsd_angstrom))
    
    # Plot Frames on X, RMSD on Y
    plt.plot(frames, rmsd_angstrom, color=colors[label], linewidth=2.5, alpha=0.9, label=label)

# Formatting the plot
plt.title("Protein Backbone RMSD Comparison (Pulling Phase)", fontsize=18, pad=15)
plt.xlabel("Frame", fontsize=14)
plt.ylabel("RMSD (Å)", fontsize=14)

# Add a dashed line showing the 2.0 Angstrom stability limit
plt.axhline(y=2.0, color='gray', linestyle='--', alpha=0.8, linewidth=2, label='2.0 Å Stability Threshold')

# Set Y-axis to a reasonable scale so the lines are easy to see
plt.ylim(0, 3.0) 

plt.legend(loc='lower right', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()

# Save the plot
plt.savefig("../plots_and_pictures/rmsd_comparison_all.png", dpi=300)
plt.show()