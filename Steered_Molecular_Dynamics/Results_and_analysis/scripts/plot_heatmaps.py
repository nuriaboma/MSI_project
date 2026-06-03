import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os

def parse_distances(filepath):
    """Parses the distance data from the Tcl-generated contacts.txt"""
    if not os.path.exists(filepath):
        return None
        
    with open(filepath) as f:
        content = f.read()

    blocks = re.split(r'freeSelLabel (.*?)\n', content)
    
    residue_labels = []
    distance_matrix = []

    for i in range(1, len(blocks)-1, 2):
        label = blocks[i].strip()
        data_block = blocks[i+1].strip().splitlines()

        match = re.search(r'([A-Z]+)\s+(\d+)', label)
        if match:
            residue_labels.append(f"{match.group(1)}{match.group(2)}")
        else:
            residue_labels.append(label)

        values = []
        for line in data_block:
            parts = line.strip().split()
            if len(parts) == 2:
                values.append(float(parts[1]))
        distance_matrix.append(values)

    df = pd.DataFrame(distance_matrix, index=residue_labels)
    return df

# Define the paths 
heatmap_data = {
    'MOD1_Replica3': '../../3PBL-MOD/MOD1/results_repl3_MOD1/contacts_MOD1.txt',
    'MOD2_Replica3': '../../3PBL-MOD/MOD2/results_repl3_MOD2/contacts_MOD2.txt'
}

ps_per_frame = 10 

for title, filepath in heatmap_data.items():
    df = parse_distances(filepath)
    
    if df is None:
        print(f"Missing data for {title}. Please check the file path: {filepath}")
        continue

    plt.figure(figsize=(14, 9))

    sns.heatmap(df, 
                cmap="magma_r", 
                vmax=12.0, 
                cbar_kws={'label': 'Distance to ligand (Å)'})

    plt.title(f"Protein-Ligand Dissociation Heatmap ({title})", fontsize=20, pad=20)
    plt.ylabel("Residue", fontsize=16)
    plt.xlabel("Time (ps)", fontsize=16)

    xticks = range(0, df.shape[1], 10)
    
    plt.xticks(
        ticks=xticks,
        labels=[str(i * ps_per_frame) for i in xticks],
        rotation=45,
        ha='right', 
        fontsize=12
    )

    plt.yticks(rotation=0, fontsize=11)
    
    plt.tight_layout(pad=2.0)

    output_filename = f"../plots_and_pictures/heatmap_{title}.png"
    plt.savefig(output_filename, dpi=300)
    
    plt.show()