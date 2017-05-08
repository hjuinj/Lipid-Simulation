import numpy as np
import MDAnalysis
import matplotlib.pyplot as plt

def a2n(length):    return length / 10.0

################################################################################
"""
Mapping out the distance between the end of the peptides
"""
dir_xtc = '/home/shuzhe/Simulations/polymerPrep/161018w2/md_prod.xtc'
dir_gro = '/home/shuzhe/Simulations/polymerPrep/161018w2/md_prod.gro'

u = MDAnalysis.Universe(dir_gro, dir_xtc)
len(u.trajectory)
peptide = u.select_atoms("resname PEP")
data = np.array([(u.trajectory.time, peptide.radius_of_gyration()) for ts in u.trajectory])
time, RG = data.T
plt.plot(time, RG)
plt.show()


################################################################################

combined = MDAnalysis.Universe(dir_combined)
max(combined.atoms.positions[:,0]) - min(combined.atoms.positions[:,0])

pep.atoms.center_of_geometry()
lipid = combined.select_atoms("resname DPPC")
c20 = combined.select_atoms("name C20")
list(c20.ids)
lipid_center_z = lipid.center_of_mass()[2]

water.resids[water.atoms.positions[:, 2] > lipid_center_z]
output = c20.ids[c20.atoms.positions[:,2] > lipid_center_z]
" ".join(map(str, output))
plt.plot(water.atoms.positions[:, 2], "o")
plt.show()
