#!/usr/bin/env python
import numpy as np
import MDAnalysis
import warnings
import subprocess, os, StringIO, re, datetime, time, sys
import optparse

def concat(u1, u2):
    """Concatenate two MDAnalysis universes

    Parameters
    ----------
    u1 : MDAnalysis universe
        First universe to be put together


    u2 : MDAnalysis universe
        Second universe to be put together

    Returns
    -------
    u_comb : MDAnalysis universe
        Combined universes

    """
    u_comb = MDAnalysis.Merge(u1, u2)
    p1 = u_comb.select_atoms("bynum 1:%s" %str(len(u1)))
    p2 = u_comb.select_atoms("bynum %s:%s" %(str(len(u1) + 1), str(len(u1) + len(u2))))
    p1.segids = "A"
    p2.segids = "B"
    p2.residues.set_resid(p2.residues.resids + p1.residues.resids[-1])
    return u_comb

def construct(entry, write_to):
    """Construct a linear polymer of a given composition based on the monomer sequence provided

    Parameters
    ----------
    entry : list of strings
        The ordered sequence of monomers to be joined together

    write_to: string
        The path to which output pdb will be written to

    Returns
    -------
        None

    """
    mapping = {
        "MA0" : os.path.abspath(os.path.join('.')) + "/MA0.pdb",
        "MA1" : os.path.abspath(os.path.join('.')) + "/MA1.pdb",
        "MB0" : os.path.abspath(os.path.join('.')) + "/MB0.pdb",
        "MB1" : os.path.abspath(os.path.join('.')) + "/MB1.pdb"
        }
    for i in range(len(entry)):
        entry[i] = MDAnalysis.Universe(mapping[entry[i]])
    polymer = entry[ 0 ]
    for i in entry[ 1 : ]:
        mer = i
        N =  polymer.atoms.positions[np.where(polymer.atoms.names == "N" ), ][0][-1]
        # print N
        mer.atoms.positions = np.sum([mer.atoms.positions, N], axis = 0) + 1
        polymer = concat(polymer.atoms, mer.atoms)
    polymer.atoms.segids = "A"
    polymer.atoms.write(write_to)
    return

"""
Example usage:

construct(["MB1"] * 5 , "./MB1x5.pdb")

"""
