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
Compare shape change of buffered and non buffered solutions
"""

def center_mol(mol, box_dim, center =  None):
    """
    Does not really work
    """
    if center is None:
        center = box_dim/2.0
    com = mol.center_of_mass()
    # if com[0] > center[0]:
    #     mol.positions[ : , 0] -= (com[0] - center[0])
    # elif com[0] < center[0]:
    #     mol.positions[ : , 0] += (center[0] - com[0])
    mol.positions = mol.positions + (center - com)
    x,y,z = mol.positions[:, 0], mol.positions[:, 1], mol.positions[:, 2]
    # xyz[:, 0][xyz[:, 0] > box_dim[0]] -= box_dim[0]
    # xyz[:, 1][xyz[:, 1] > box_dim[1]] -= box_dim[1]
    # xyz[:, 2][xyz[:, 2] > box_dim[2]] -= box_dim[2]
    # xyz[:, 0][xyz[:, 0] < 0] += box_dim[0]
    # xyz[:, 1][xyz[:, 1] < 0] += box_dim[1]
    # xyz[:, 2][xyz[:, 2] < 0] += box_dim[2]
    # mol.positions = xyz
    x[x > box_dim[0]] -= box_dim[0]
    x[x < 0] += box_dim[0]
    print x[x > box_dim[0]]
    print x[x < 0]
    y[y > box_dim[1]] -= box_dim[1]
    y[y < 0] += box_dim[1]
    print y[y > box_dim[1]]
    print y[y < 0]
    z[z > box_dim[2]] -= box_dim[2]
    z[z < 0] += box_dim[2]
    print z[z > box_dim[2]]
    print z[z < 0]
    mol.positions = np.transpose(np.array([x, y ,z]))
    print mol.center_of_mass()
    print
    return mol



u = MDAnalysis.Universe("/home/shuzhe/Simulations/22week/8.MA0x5_solv_with_buffer/Output/npt.gro", "/home/shuzhe/Simulations/22week/8.MA0x5_solv_with_buffer/Output/centered.xtc")

MA0x5_buffer = u.select_atoms("resname MA0")
MA0x5_buffer
dim = u.dimensions[0:3]
middle = dim/2.0
Asphere = []
for ts in u.trajectory:
    # MA0x5_buffer.
    # MA0x5_buffer = center_mol(MA0x5_buffer, dim, middle)
    # print MA0x5_buffer.center_of_mass()
    # Asphere.append((u.trajectory.time, np.sum(MA0x5_buffer.center_of_mass())))
    Asphere.append((u.trajectory.time, MA0x5_buffer.asphericity(pbc = True)))
Asphere = np.array(Asphere)

u = MDAnalysis.Universe("/home/shuzhe/Simulations/22week/8.MA0x5_solv_with_buffer/Output/npt.gro", "/home/shuzhe/Simulations/22week/8.MA0x5_solv_with_buffer/Output/centered.xtc")
def obtain_asphericity_change(u, mol):
    MA0x5_buffer = u.select_atoms("resname " + str(mol))
    dim = u.dimensions[0:3]
    middle = dim/2.0
    Asphere = []
    for ts in u.trajectory:
        Asphere.append((u.trajectory.time, MA0x5_buffer.asphericity(pbc = True)))
    Asphere = np.array(Asphere)
    return Asphere



u = MDAnalysis.Universe("/home/shuzhe/Simulations/22week/8.MA0x5_solv_with_buffer/Output/npt.gro", "/home/shuzhe/Simulations/22week/8.MA0x5_solv_with_buffer/Output/centered.xtc")
MA0 = obtain_asphericity_change(u, "MA0")
ax = plt.subplot(4, 1, 1)
ax.plot(MA0[:,0], MA0[:,1], 'r--', lw=2, label=r"$R_G$")
ax.set_xlabel("time (ps)")
ax.set_ylabel(r"Asphericity")

u = MDAnalysis.Universe("/home/shuzhe/Simulations/22week/9.MA1x5_solv_with_buffer/Output/npt.gro", "/home/shuzhe/Simulations/22week/9.MA1x5_solv_with_buffer/Output/centered.xtc")
MA1 = obtain_asphericity_change(u, "MA1")
ax = plt.subplot(4, 1, 2)
ax.plot(MA1[:,0], MA1[:,1], 'g--', lw=2, label=r"$R_G$")
ax.set_xlabel("time (ps)")
ax.set_ylabel(r"Asphericity")

u = MDAnalysis.Universe("/home/shuzhe/Simulations/22week/10.MB0x5_solv_with_buffer/Output/npt.gro", "/home/shuzhe/Simulations/22week/10.MB0x5_solv_with_buffer/Output/centered.xtc")
MB0 = obtain_asphericity_change(u, "MB0")
ax = plt.subplot(4, 1, 3)
ax.plot(MB0[:,0], MB0[:,1], 'g--', lw=2, label=r"$R_G$")
ax.set_xlabel("time (ps)")
ax.set_ylabel(r"Asphericity")

u = MDAnalysis.Universe("/home/shuzhe/Simulations/22week/11.MB1x5_solv_with_buffer/Output/npt.gro", "/home/shuzhe/Simulations/22week/11.MB1x5_solv_with_buffer/Output/centered.xtc")
MB1 = obtain_asphericity_change(u, "MB1")
ax = plt.subplot(4, 1, 4)
ax.plot(MB1[:,0], MB1[:,1], 'g--', lw=2, label=r"$R_G$")
ax.set_xlabel("time (ps)")
ax.set_ylabel(r"Asphericity")
plt.show()

plt.semilogy(MA0[:, 0], MA0[:, 1], "r--", MA1[:, 0], MA1[:, 1], "g--", MB0[:, 0], MB0[:, 1], "b--", MB1[:, 0], MB1[:, 1], "y--")
plt.show()
