
# SMD Simulation: Ligand Unbinding Report & README

## 1. Overview
This simulation uses **Steered Molecular Dynamics (SMD)** to study the dissociation of a ligand from its receptor. Unlike classical MD, an external force is applied to pull the ligand out of the binding pocket along a specific reaction coordinate (the Z-axis). This allows us to calculate the **Potential of Mean Force (PMF)** and evaluate binding affinity.

## 2. Need for the production files
To run GROMACS for the SMD part it is needed the output files from teh production step. To do so, these comands were used
````