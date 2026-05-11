# $Id: smd.tcl,v 1.2 2005/02/18 18:07:11 mbach Exp $

# List of ligand atoms (IDs obtained from VMD). Exclude the massless lone pair site.
set ligand_atoms {3939 3940 3941 3942 3943 3944 3945 3946 3947 3948 3949 3950 3951 3952 3953 3954 3955 3956 3957 3958 3959 3960 3961 3962 3963 3964 3965 3966 3967 3968 3969 3970 3971 3972 3973 3974 3975 3976 3977 3978 3979 3980 3981 3982 3983 3984 3985 3986 3987 3988}

# Create a group with all ligand atoms
set a2 [addgroup $ligand_atoms]

# Simulation parameters
set Tclfreq 50
set t 0
set k 7.2        ;# Force constant (kcal/mol/Å²)
set v 0.00002    ;# Pulling velocity (Å/timestep)
set target_z 90.0

# Output file
set outfilename ligand_smd.out
open $outfilename w

# Function to calculate COM Z using the "coor" array (valid in NAMD Tcl)
proc calcCOMZ_simple { group } {
    loadcoords coor
    set sum_z 0.0
    set n 0

    foreach atom $group {
        set z [lindex $coor($atom) 2]
        set sum_z [expr {$sum_z + $z}]
        incr n
    }

    return [expr {$sum_z / double($n)}]
}

# Main function to apply the force
proc calcforces {} {

  global Tclfreq t k v a2 target_z outfilename

  # Update coordinates and dynamically calculate COM Z
  set comz [calcCOMZ_simple $a2]

  # Target Z coordinate for this step
  set target_current_z [expr {$comz + ($v * $t)}]

  # Calculate force
  set fz [expr {$k * ($target_current_z - $comz)}]

  # Avoid NaN values
  if { $fz != $fz } {
      puts "ERROR: fz is NaN, ending simulation"
      exit
  }

  # Apply force
  set force [list 0.0 0.0 $fz]
  addforce $a2 $force

  # Save results every Tclfreq steps
  if { [expr {$t % $Tclfreq}] == 0 } {
      set outfile [open $outfilename a]
      set time [expr {$t*2/1000.0}]  ;# Convert timesteps to ps
      puts $outfile "$time $comz $fz"
      close $outfile
  }

  # Stop if target Z is reached
  if { $comz >= $target_z } {
      puts "SMD finished: Ligand reached Z = $target_z Å"
      exit
  }

  incr t
  return
}

