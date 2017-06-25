import numpy as np
import pickle
import MDAnalysis
import matplotlib.pyplot as plt
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pandas as pd
    import subprocess, os, StringIO, re, datetime, time, sys
import optparse
# a = pd.DataFrame([[0,0,0]], columns = [1,2,3])
# a
#
# a.to_csv("./log.log", sep = "\t", index = True, header = True)
# a=pd.read_csv("./log.log", sep = "\t", index_col = 0, header = 0)
# a
# b = pd.DataFrame([[1,1,1]], columns = [1,2,3])
# a.append(b, ignore_index = True)

from MDAnalysis import *
from MDAnalysis.analysis.align import *
MDAnalysis.core.flags['use_periodic_selections'] = True
MDAnalysis.core.flags['use_KDTree_routines'] = False

def select_nearby_lipid(frame, polymer, r = 20, z_min = -90, z_max = -90):
    # ids = frame.select_atoms("cyzone %d %d %d %s" %(r, z_min, z_max, polymer))
    upper = select_upper_lipid(frame)
    lipids = frame.select_atoms("resname is DPPC")
    ids = frame.select_atoms("sphzone %d (resname  %s )" %(r,  polymer))

    ids = ids.select_atoms("resname is DPPC").resids
    ids = [str(i) for i in ids]
    cmd = " or ".join([ "resid " + i for i in (ids)])
    nearby = upper.select_atoms(cmd)
    return nearby

def select_not_nearby_lipid(frame, polymer, r = 20, z_min = -90, z_max = -90):
    # ids = frame.select_atoms("cyzone %d %d %d %s" %(r, z_min, z_max, polymer))
    upper = select_upper_lipid(frame)
    lipids = frame.select_atoms("resname is DPPC")
    ids = frame.select_atoms("( sphzone %d (resname  %s ))" %(r,  polymer))

    ids = ids.select_atoms("resname is DPPC").resids
    ids = [str(i) for i in ids]
    cmd = " or ".join([ "resid " + i for i in (ids)])
    nearby = upper.select_atoms("not ( %s )" %(cmd))
    return nearby

def select_upper_lipid(frame):
    lipids = frame.select_atoms("resname is DPPC")
    com = lipids.center_of_mass()[2]
    ids = lipids.select_atoms("name is P8 and prop z >= " + str(com)).resids
    ids = [str(i) for i in ids]
    cmd = " or ".join([ "resid " + i for i in (ids)])
    upper = lipids.select_atoms(cmd)
    return upper

def lipid_P(lipids, P = "P8"):
    P = lipids.select_atoms("name is " + P)
    return P


def get_distance_for_timestep(group1, group2): #TODO implement for xyz directions
    ids = set(group1.atoms.resids)
    assert(ids == set(group2.atoms.resids))
    distance =  []

    for i in ids:
        a = group1.select_atoms("resid " + str(i)).positions
        b = group2.select_atoms("resid " + str(i)).positions
        distance.append(xy_distance(a,b))
    return distance

def xy_distance(atom1, atom2):
    tmp = atom1.positions - atom2.positions
    np.linalg.norm(tmp[0:2])

def get_displacement(path, gro_file = "/mdrun.gro", xtc_file = "/mdrun.xtc"):
    trj = MDAnalysis.Universe(path + gro_file , path + xtc_file)
    P = lipid_P(select_upper_lipid(trj))
    output = []
    for ts in trj.trajectory:
        output += get_angles_from_norm(middle,tail)
    return output


def lipid_regions(lipids, head = ["C1", "C2", "C3", "N4", "C5", "C6" ], middle = ["O7", "P8", "O9", "O10", "O11"]):
    tail = lipids.select_atoms("not(" + " or ".join(["name is " + i for i in middle + head]) + ")")
    head = lipids.select_atoms(" or ".join(["name is " + i for i in head]))
    middle = lipids.select_atoms(" or ".join(["name is " + i for i in middle]))
    return head, middle, tail



def get_angle_helper(u, v):
    from numpy import (array, dot, arccos, clip, degrees)
    from numpy.linalg import norm
    c = dot(u,v)/norm(u)/norm(v) # -> cosine of the angle
    angle = arccos(clip(c, -1, 1)) # if you really want the angle
    return degrees(angle)


def get_PN_angles_from_norm(frame, norm = [0, 0, 1.]):
    ids = set(frame.atoms.resids)
    angles =  []

    P = frame.select_atoms("name is P8")
    N = frame.select_atoms("name is N4")
    for i in ids:
        a = N.select_atoms("resid " + str(i)).center_of_mass()
        b = P.select_atoms("resid " + str(i)).center_of_mass()
        c = a - b
        angles.append(get_angle_helper(c,norm))
    return angles

def get_angles_from_norm(head, middle, tail, norm = [0, 0, 1.]):
    ids = set(middle.atoms.resids)
    angles =  []
    assert(ids == set(tail.atoms.resids))

    for i in ids:
        a = middle.select_atoms("resid " + str(i)).center_of_mass()
        b = tail.select_atoms("resid " + str(i)).center_of_mass()
        c = a - b
        angles.append(get_angle_helper(c,norm))
    return angles

def get_angles_between_head_middle_tail(head, middle, tail):
    ids = set(head.atoms.resids)
    angles =  []

    for i in ids:
        a =head.select_atoms("resid " + str(i)).center_of_mass()
        b = middle.select_atoms("resid " + str(i)).center_of_mass()
        c = tail.select_atoms("resid " + str(i)).center_of_mass()
        angles.append(get_angle_helper(a-b,c-b))
    return angles

plt.hist(get_angles_between_head_middle_tail(head, middle, tail))
plt.show()
##################33
"""
Extract different files
"""
import os
import re
def get_immediate_subdirectories_with_pattern(a_dir, pattern = "Output_frame"):
    tmp = [name for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir, name)) and name.startswith(pattern)]
    # return [a_dir + i for i in sorted(tmp, key = lambda key : int(re.findall(r'\d+', key)[0]))]
    return sorted(tmp, key = lambda key : int(re.findall(r'\d+', key)[0]))


get_immediate_subdirectories_with_pattern("/home/shuzhe/Simulations/23week/7.MA0x5_DPPC_US_ion/")


def get_orientations(path, gro_file = "/mdrun.gro", xtc_file = "/mdrun.xtc"):
    trj = MDAnalysis.Universe(path + gro_file , path + xtc_file)
    head, middle, tail = lipid_regions(select_upper_lipid(trj))
    output = []
    for ts in trj.trajectory:
        output += get_angles_from_norm(head, middle,tail)
    return output

def get_PN_orientations(path, gro_file = "/mdrun.gro", xtc_file = "/mdrun.xtc"):
    trj = MDAnalysis.Universe(path + gro_file , path + xtc_file)
    output = []
    for ts in trj.trajectory:
        output += get_PN_angles_from_norm(select_upper_lipid(trj))
    return output

def get_orientations_2(path, gro_file = "/mdrun.gro", xtc_file = "/mdrun.xtc"):
    trj = MDAnalysis.Universe(path + gro_file , path + xtc_file)
    head, middle, tail = lipid_regions(select_upper_lipid(trj))
    output = []
    for ts in trj.trajectory:
        output += get_angles_between_head_middle_tail(head,middle,tail)
    return output

def get_orientations_3(path, gro_file = "/mdrun.gro", xtc_file = "/mdrun.xtc", **kwargs):
    trj = MDAnalysis.Universe(path + gro_file , path + xtc_file)
    output1 = []
    tmp = select_nearby_lipid(trj, **kwargs)
    head, middle, tail = lipid_regions(tmp)
    for ts in trj.trajectory:
        output += get_angles_between_head_middle_tail(head,middle,tail)

    # head, middle, tail = lipid_regions(select_not_nearby_lipid(select_upper_lipid(trj), **kwargs))
    # output2 = []
    # for ts in trj.trajectory:
    #     output += get_angles_between_head_middle_tail(head,middle,tail)
    # return [output1, output2]
    return output1

def lipid_thickness(lipids, P = "P8"):
    lipids =  lipid_P(lipids)
    z = lipids.atoms.center_of_mass()[2]
    upper = lipids.select_atoms("prop z >= " + str(z))
    n = len(upper.atoms.positions[:,0])
    lower = lipids.select_atoms("prop z < " + str(z))
    return (sum(upper.atoms.positions[:, 2]) - sum(lower.atoms.positions[:, 2]))/n

def get_lipid_thickness(path, gro_file = "/mdrun.gro", xtc_file = "/mdrun.xtc"):
    trj = MDAnalysis.Universe(path + gro_file , path + xtc_file)
    output = []
    for ts in trj.trajectory:
        output.append(lipid_thickness(trj))
    return output


def make_df(path, sub_dirs, func = get_orientations, **kwargs) :
    df = []
    for i in sub_dirs:
        print i
        df.append( (i, func(path + i, **kwargs)))
    return df


def get_orientations_3(path, gro_file = "/mdrun.gro", xtc_file = "/mdrun.xtc", **kwargs):
    trj = MDAnalysis.Universe(path + gro_file , path + xtc_file)
    output = []
    for ts in trj.trajectory:
        # output.append(lipid_thickness(trj))
        print select_nearby_lipid(trj, **kwargs)
    # return output
path = "/home/shuzhe/Simulations/23week/7.MA0x5_DPPC_US_ion/"
get_orientations_3(path + "Output_frame50/", polymer = "MA0")
x = make_df(path, get_immediate_subdirectories_with_pattern(path), get_nearby_lipids, polymer = "MA0")




x = make_df(path, get_immediate_subdirectories_with_pattern(path))


MA0 = x
pickle.dump(MA0, open("./Analysis/MA0.pickle", "wb"))


##########################################################
#########################################################
"""
        Angle between head-middle and middle-tail
"""

path = "/home/shuzhe/Simulations/23week/7.MA0x5_DPPC_US_ion/"
MA0_angle = make_df(path, get_immediate_subdirectories_with_pattern(path), func = get_orientations_2)
pickle.dump(MA0_angle, open("./MA0_angle.pickle", "wb"))


path = "/home/shuzhe/Simulations/25week/10.MA1x5_US/"
MA1_angle = make_df(path, get_immediate_subdirectories_with_pattern(path), func = get_orientations_2)
pickle.dump(MA1_angle, open("./MA1_angle.pickle", "wb"))

path = "/home/shuzhe/Simulations/25week/1.MB0x5_DPPC_US_ion/"
MB0_angle = make_df(path, get_immediate_subdirectories_with_pattern(path), func = get_orientations_2)
pickle.dump(MB0_angle, open("./MB0_angle.pickle", "wb"))

path = "/home/shuzhe/Simulations/25week/11.MB1x5_US/"
MB1_angle = make_df(path, get_immediate_subdirectories_with_pattern(path), func = get_orientations_2)
pickle.dump(MB1_angle, open("./MB1_angle.pickle", "wb"))
##########################################################

##########################################################
#########################################################
"""
        lipid thickness records
"""

path = "/home/shuzhe/Simulations/23week/7.MA0x5_DPPC_US_ion/"
thick_MA0 = make_df(path, get_immediate_subdirectories_with_pattern(path), func = get_lipid_thickness)
pickle.dump(thick_MA0, open("./Analysis/thick_MA0.pickle", "wb"))

thick_MA0[11][1]


path = "/home/shuzhe/Simulations/25week/10.MA1x5_US/"
thick_MA1 = make_df(path, get_immediate_subdirectories_with_pattern(path), func = get_lipid_thickness)
pickle.dump(thick_MA1, open("./Analysis/thick_MA1.pickle", "wb"))

path = "/home/shuzhe/Simulations/25week/1.MB0x5_DPPC_US_ion/"
thick_MB0 = make_df(path, get_immediate_subdirectories_with_pattern(path), func = get_lipid_thickness)
pickle.dump(thick_MB0, open("./Analysis/thick_MB0.pickle", "wb"))

path = "/home/shuzhe/Simulations/25week/11.MB1x5_US/"
thick_MB1 = make_df(path, get_immediate_subdirectories_with_pattern(path), func = get_lipid_thickness)
pickle.dump(thick_MB1, open("./Analysis/thick_MB1.pickle", "wb"))
##########################################################



##########################################################
#########################################################
"""
        Angle for P-N and normal
"""

path = "/home/shuzhe/Simulations/23week/7.MA0x5_DPPC_US_ion/"
MA0_PN_angle = make_df(path, get_immediate_subdirectories_with_pattern(path), func = get_PN_orientations)
pickle.dump(MA0_PN_angle, open("./MA0_PN_angle.pickle", "wb"))


path = "/home/shuzhe/Simulations/25week/10.MA1x5_US/"
MA1_PN_angle = make_df(path, get_immediate_subdirectories_with_pattern(path), func = get_PN_orientations)
pickle.dump(MA1_PN_angle, open("./MA1_PN_angle.pickle", "wb"))

path = "/home/shuzhe/Simulations/25week/1.MB0x5_DPPC_US_ion/"
MB0_PN_angle = make_df(path, get_immediate_subdirectories_with_pattern(path), func = get_PN_orientations)
pickle.dump(MB0_PN_angle, open("./MB0_PN_angle.pickle", "wb"))

path = "/home/shuzhe/Simulations/25week/11.MB1x5_US/"
MB1_PN_angle = make_df(path, get_immediate_subdirectories_with_pattern(path), func = get_PN_orientations)
pickle.dump(MB1_PN_angle, open("./MB1_PN_angle.pickle", "wb"))
##########################################################







x[0][1]










plt.hist(x[0][1], bins = 'auto')
#set_xlabel("time (ps)")
#set_ylabel(r"Asphericity")
#plt.xlim([0,1])
plt.show()
##############

path = "/home/shuzhe/Simulations/23week/3.MA0x5_DPPC_US/Output_frame5/"
trj = MDAnalysis.Universe(path + "mdrun.gro" , path + "mdrun.xtc")
head, middle, tail = lipid_regions(select_upper_lipid(trj))
output = []
for ts in trj.trajectory:
    output += get_angles_from_norm(middle,tail)
len(trj.trajectory)
a = trj.trajectory[2]
b = trj.trajectory[200]
print a

plt.hist(output, bins = 'auto')
#set_xlabel("time (ps)")
#set_ylabel(r"Asphericity")
#plt.xlim([0,1])
plt.show()


path = "/home/shuzhe/Simulations/23week/3.MA0x5_DPPC_US/Output_frame60/"
trj = MDAnalysis.Universe(path + "mdrun.gro" , path + "mdrun.xtc")
head, middle, tail = lipid_regions(select_upper_lipid(trj))
output = []
for ts in trj.trajectory:
    output += get_angles_from_norm(middle,tail)

plt.hist(output, bins = 'auto')
#set_xlabel("time (ps)")
#set_ylabel(r"Asphericity")
#plt.xlim([0,1])
plt.show()
