#!/usr/bin/env python
import numpy as np
import MDAnalysis
import matplotlib.pyplot as plt
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pandas as pd
import subprocess, os, StringIO, re, datetime, time, sys
import optparse

"""

gmx pdb2gmx -f XXZ.pdb  -o XXZ.gro -water spce -inter -missing
gmx editconf -d 1 -f XXZ.gro -o XXZ_box.gro -c -bt cubic
gmx grompp -f 0-emin.mdp -c XXZ_box.gro -p topol.top -o XXZ_min.tpr


MA0 = MDAnalysis.Universe("/home/shuzhe/Simulations/RESOURCES/models/MA0.pdb")
C =  MA0.atoms.positions[np.where(MA0.atoms.names == "C" ), ]
MA0.atoms.positions  = np.diff([MA0.atoms.positions, C], axis = 0)[0][0]
MA0.atoms.write("/home/shuzhe/Simulations/RESOURCES/models/MA0.pdb")

MA0 = MDAnalysis.Universe("/home/shuzhe/Simulations/RESOURCES/models/MA0.pdb")
MA1 = MDAnalysis.Universe("/home/shuzhe/Simulations/RESOURCES/models/MA1.pdb")
C =  MA1.atoms.positions[np.where(MA1.atoms.names == "C" ), ]
MA1.atoms.positions  = np.diff([MA1.atoms.positions, C], axis = 0)[0][0]
MA1.atoms.write("/home/shuzhe/Simulations/RESOURCES/models/MA1.pdb")

MA0 = MDAnalysis.Universe("/home/shuzhe/Simulations/RESOURCES/models/MA0.pdb")
MA1 = MDAnalysis.Universe("/home/shuzhe/Simulations/RESOURCES/models/MA1.pdb")
MB0 = MDAnalysis.Universe("/home/shuzhe/Simulations/RESOURCES/models/MB0.pdb")
C =  MB0.atoms.positions[np.where(MB0.atoms.names == "C" ), ]
MB0.atoms.positions  = np.diff([MB0.atoms.positions, C], axis = 0)[0][0]
MB0.atoms.write("/home/shuzhe/Simulations/RESOURCES/models/MB0.pdb")

MA0 = MDAnalysis.Universe("/home/shuzhe/Simulations/RESOURCES/models/MA0.pdb")
MA1 = MDAnalysis.Universe("/home/shuzhe/Simulations/RESOURCES/models/MA1.pdb")
MB0 = MDAnalysis.Universe("/home/shuzhe/Simulations/RESOURCES/models/MB0.pdb")
MB1 = MDAnalysis.Universe("/home/shuzhe/Simulations/RESOURCES/models/MB1.pdb")
C =  MB1.atoms.positions[np.where(MB1.atoms.names == "C" ), ]
MB1.atoms.positions  = np.diff([MB1.atoms.positions, C], axis = 0)[0][0]
MB1.atoms.write("/home/shuzhe/Simulations/RESOURCES/models/MB1.pdb")
""""
def concat(u1, u2):
    u_comb = MDAnalysis.Merge(u1, u2)
    p1 = u_comb.select_atoms("bynum 1:%s" %str(len(u1)))
    p2 = u_comb.select_atoms("bynum %s:%s" %(str(len(u1) + 1), str(len(u1) + len(u2))))
    p1.segids = "A"
    p2.segids = "B"
    p2.residues.set_resid(p2.residues.resids + p1.residues.resids[-1])
    return u_comb

mapping = {
    "MA0" : "/home/shuzhe/Simulations/RESOURCES/models/MA0.pdb",
    "MA1" : "/home/shuzhe/Simulations/RESOURCES/models/MA1.pdb",
    "MB0" : "/home/shuzhe/Simulations/RESOURCES/models/MB0.pdb",
    "MB1" : "/home/shuzhe/Simulations/RESOURCES/models/MB1.pdb",
    }
# MA0 = MDAnalysis.Universe("/home/shuzhe/Simulations/RESOURCES/models/MA0.pdb")
# MA1 = MDAnalysis.Universe("/home/shuzhe/Simulations/RESOURCES/models/MA1.pdb")
# MB0 = MDAnalysis.Universe("/home/shuzhe/Simulations/RESOURCES/models/MB0.pdb")
# MB1 = MDAnalysis.Universe("/home/shuzhe/Simulations/RESOURCES/models/MB1.pdb")

# entry = [MA0, MA1, MB0, MB1, MA0, MA1, MB0, MB1]
# entry = [MA0] * 5

def construct(entry, write_to):
    for i in range(len(entry)):
        entry[i] = MDAnalysis.Universe(mapping[entry[i]])
    polymer = entry[ 0 ]
    for i in entry[ 1 : ]:
        mer = i
        N =  polymer.atoms.positions[np.where(polymer.atoms.names == "N" ), ][0][-1]
        print N
        mer.atoms.positions = np.sum([mer.atoms.positions, N], axis = 0) + 1
        polymer = concat(polymer.atoms, mer.atoms)
    polymer.atoms.segids = "A"
    polymer.atoms.write(write_to)
    return

construct(["MB1"] * 5 , "/home/shuzhe/Simulations/21week/MB1x5.pdb")
#############################################
MA0
terminals =  np.where(MA0.atoms.names == "N" ) + np.where(MA0.atoms.names == "C" )
MA0.atoms.positions[terminals, ]
np.diff(MA0.atoms.positions[terminals, ], axis = 0)

#############################################

#############################################
MA1
terminals =  np.where(MA1.atoms.names == "N" ) + np.where(MA1.atoms.names == "C" )
MA1.atoms.positions[terminals, ]
np.diff(MA1.atoms.positions[terminals, ], axis = 0)

#############################################
#############################################
MB0
terminals =  np.where(MB0.atoms.names == "N" ) + np.where(MB0.atoms.names == "C" )
MB0.atoms.positions[terminals, ]
np.diff(MB0.atoms.positions[terminals, ], axis = 0)

#############################################
#############################################
MB1
terminals =  np.where(MB1.atoms.names == "N" ) + np.where(MB1.atoms.names == "C" )
MB1.atoms.positions[terminals, ]
np.diff(MB1.atoms.positions[terminals, ], axis = 0)

#############################################
peptide = MDAnalysis.Universe("/home/shuzhe/Simulations/19week/6.Concat_peptides/XXZ_neutral_mono.pdb")
for i in range(6):
    print i
    mer = MDAnalysis.Universe("/home/shuzhe/Simulations/19week/6.Concat_peptides/XXZ_neutral_mono.pdb")
    mer.atoms.positions += (1 + i)
    peptide = concat(peptide.atoms, mer.atoms)

peptide.atoms.segids = "A"
peptide.atoms.write("/home/shuzhe/Simulations/19week/6.Concat_peptides/tmp.pdb")

##########################################3
peptide2.atoms.positions += 1
join = concat(peptide2.atoms, peptide.atoms)
join.atoms
join.atoms.resids
for a in  join.atoms:
    print a
join.atoms.segids = "A"
join.atoms.write("/home/shuzhe/Simulations/19week/6.Concat_peptides/tmp.pdb")
