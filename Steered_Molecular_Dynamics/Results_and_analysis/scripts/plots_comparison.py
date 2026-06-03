import os
import numpy as np
import matplotlib.pyplot as plt

def read_xvg(filepath, col):
    """Reads a GROMACS .xvg file and extracts a specific column."""
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

# Define the ligands and colors for plotting
ligands = ['ETQ', 'MOD1', 'MOD2']
colors = {'ETQ': 'black', 'MOD1': 'blue', 'MOD2': 'red'}
replicas = [1, 2, 3]

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for lig in ligands:
    lig_force = []
    lig_work = []
    lig_ext = []
    lig_time = []
    
    for rep in replicas:
        # Paths to the data files based on ligand and replica
        if lig == 'ETQ':
            folder = f"../../3PBL-ETQ/results/run{rep}_gpu"
            prefix = f"smd_replica{rep}"
        elif lig == 'MOD1':
            folder = f"../../3PBL-MOD/MOD1/results_repl{rep}_MOD1"
            prefix = f"smd_repl{rep}_MOD1"
        elif lig == 'MOD2':
            folder = f"../../3PBL-MOD/MOD2/results_repl{rep}_MOD2"
            prefix = f"smd_repl{rep}_MOD2"
        
        f_file = f"{folder}/{prefix}_pullf.xvg"
        x_file = f"{folder}/{prefix}_pullx.xvg"
        
        force = read_xvg(f_file, 1)
        pos = read_xvg(x_file, 1)
        time = read_xvg(x_file, 0)
        
        if force is None or pos is None:
            print(f"Missing data for {lig} replica {rep}. Skipping.")
            continue
            
        # Calculate Extension in Angstroms
        start_pos = pos[0]
        extension = (pos - start_pos) * 10.0
        
        # Calculate Work (PMF)
        work = [0.0]
        cumulative_w = 0.0
        for i in range(1, len(force)):
            dx = (extension[i] - extension[i-1]) / 10.0
            avg_f = (force[i] + force[i-1]) / 2.0
            cumulative_w += avg_f * dx
            work.append(cumulative_w)
            
        # Store data for averaging
        lig_force.append(force)
        lig_work.append(np.array(work))
        lig_ext.append(extension)
        lig_time.append(time)
        
        # Plot individual replicas 
        axes[0].plot(extension, force, color=colors[lig], alpha=0.25, linewidth=1)
        axes[1].plot(extension, work, color=colors[lig], alpha=0.25, linewidth=1)
        axes[2].plot(time, extension, color=colors[lig], alpha=0.25, linewidth=1)

    # --- COMPUTE THE AVERAGES OF THE REPLICAS ---
    if len(lig_force) > 0:
        # Find the minimum length among the 3 replicas to safely average them
        min_len = min([len(f) for f in lig_force])
        
        # Truncate all arrays to the minimum length and stack them
        trunc_force = np.vstack([f[:min_len] for f in lig_force])
        trunc_work = np.vstack([w[:min_len] for w in lig_work])
        trunc_ext = np.vstack([e[:min_len] for e in lig_ext])
        trunc_time = np.vstack([t[:min_len] for t in lig_time])
        
        # Calculate the mean across the columns
        avg_force = np.mean(trunc_force, axis=0)
        avg_work = np.mean(trunc_work, axis=0)
        avg_ext = np.mean(trunc_ext, axis=0)
        avg_time = np.mean(trunc_time, axis=0)
        
        # Plot the average line (thick and bold)
        axes[0].plot(avg_ext, avg_force, color=colors[lig], alpha=1.0, linewidth=2.5, label=f"{lig} (Avg)")
        axes[1].plot(avg_ext, avg_work, color=colors[lig], alpha=1.0, linewidth=2.5, label=f"{lig} (Avg)")
        axes[2].plot(avg_time, avg_ext, color=colors[lig], alpha=1.0, linewidth=2.5, label=f"{lig} (Avg)")

# Format the plots
axes[0].set_title("Force vs Extension", fontsize=14)
axes[0].set_xlabel("Extension (Å)")
axes[0].set_ylabel("Force (kJ/mol/nm)")
axes[0].legend()

axes[1].set_title("Work vs Extension (PMF)", fontsize=14)
axes[1].set_xlabel("Extension (Å)")
axes[1].set_ylabel("Work (kJ/mol)")
axes[1].legend()

axes[2].set_title("Time vs Extension", fontsize=14)
axes[2].set_xlabel("Time (ps)")
axes[2].set_ylabel("Extension (Å)")
axes[2].legend()

# Save the plot
plt.tight_layout()
plt.savefig("../plots_and_pictures/comparative_smd_plots_averaged.png", dpi=300)
plt.show()