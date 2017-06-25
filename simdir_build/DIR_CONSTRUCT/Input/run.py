#!/usr/bin/env python
import sys
sys.path.insert(0, '/home/sw4512/Scripts/')
sys.path.insert(0, '/home/shuzhe/Simulations/Scripts/deploy')
from MDP_Builder import *
from PBS_Builder import *

#################################### MDP FILE GENERATION ######################
mdp = MDP_Builder()
mdp.emin()
mdp.write()

mdp.nvt()
#mdp.replace_val("pcoupltype", "isotropic")
#mdp.replace_val("ref_p", "1.0")
#mdp.replace_val("compressibility", "4.5e-5")
mdp.write()

mdp.npt()
mdp.write()

mdp.production()
mdp.replace_val("nsteps", 10000000) #20 ns produciton simulation
mdp.write()
#################################### PBS FILE GENERATION ######################
pbs = PBS_Builder(mdp.counter) #any number of step below this
pbs.set_title("rename") #GIVE IT A MEANINGFUL NAME!!!!
pbs.set_cpus(20)
pbs.write_pbs("init.gro")

"""
### Umbrella Sampling
us = US_PBS_Builder(stages = 2)
us.select_frames()
#us.select_frames(start = 180, end = 480, frames = 8, pattern = "conf#.gro")
#us.set_cpus(cpu_idx = range(20), cpu_val = [20]*8)
us.write_us_pbs()

"""

#TODO smart modification of topology file
