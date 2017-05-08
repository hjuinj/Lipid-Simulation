#!/usr/bin/env python
import MDAnalysis
from MDAnalysis.analysis.align import *
from MDAnalysis.analysis.rms import rmsd

import optparse

#dir = "/home/shuzhe/Simulations/23week/12.MB0x5_solv_buffer_multi_trj/Output/"

# top = "/home/shuzhe/Simulations/23week/12.MB0x5_solv_buffer_multi_trj/Output/[____].gro"
# trj = "/home/shuzhe/Simulations/23week/12.MB0x5_solv_buffer_multi_trj/Output/[____].xtc"
# def align(top_name, trj_name, num_trj, out_name = "tmp"):
#     ref = MDAnalysis.Universe(top.replace("[____]", top_name))
#     for i in range(num_trj):
#         trjectory = MDAnalysis.Universe(top.replace("[____]", top_name), trj.replace("[____]", trj_name + "_" + str(i)))
#         align =  rms_fit_trj(trjectory, ref, filename=trj.replace("[____]", out_name + "_" + str(i)))
#

def parse():
    parser = optparse.OptionParser()
    parser.add_option("-f", dest="file1")
    parser.add_option("-g", dest="file2")
    parser.add_option("-d", dest="directory", default = "./")
    parser.add_option("-n", dest = "number")
    parser.add_option('-o', dest="output_file", default = "./output.gro")
    (options, args ) = parser.parse_args()
    return options

def align(dir, top_name, trj_name, num_trj, out_name = "msm", select = "all"):
    ref = MDAnalysis.Universe(dir + top_name + ".gro")
    for i in range(num_trj):
        print i
        trjectory = MDAnalysis.Universe(dir + top_name + ".gro", dir + trj_name + str(i) + ".xtc")
        align =  rms_fit_trj(trjectory, ref, select, filename= dir + out_name + "_" + str(i) + ".xtc")

# align("polymer", "msm", 1, "tmp", select ="name CE1 or name CF or name N1 or name CD or name CB or name N" )
#align("polymer", "tmp", 8, "msm")

options = parse()
align(options.directory, options.file1, options.file2, int(options.number))
