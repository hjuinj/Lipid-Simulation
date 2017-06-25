#!/usr/bin/env python
from collections import OrderedDict

# a = OrderedDict()
#
# # a = {     "title"       : "DEFAULT TITLE", "define"      : "-DPOSRES"}
# a["title"] = "a"
# a["define"] = "b"
#
# b = OrderedDict()
# b["c" ] = "c"
# print a
# print b
#
# a + b
# OrderedDict(a , b)
#
# for i,j in  a:
#     print i, j

"""
TODOs:
    - Add descriptions to each section of mdp file
"""


class MDP_Builder(object):
    def __init__(self, counter = 0):
        self.counter = counter
        self.to_write = OrderedDict()
        self.file_name = ""

    def combine(self, array):
        final_ordered_dict = reduce(self.combine_helper, array)
        self.to_write = final_ordered_dict

    def combine_helper(self, x, y):
        """
        x and y are ordered dictionaries
        """
        out = OrderedDict()

        for i in x:
            out[i] = x[i]
        for i in y:
            out[i] = y[i]
        return out

    def remove_key(self, key ):
        try:
            self.to_write.pop(key)
        except KeyError:
            pass

    def replace_key(self, original, new):
        self.to_write = OrderedDict([(new, v) if k == original else (k, v) for k, v in self.to_write.items()])

    def replace_val(self, key, new_val):
        new_val = str(new_val) + " "
        self.to_write[key] = new_val
        if key == "tc-grps":
            ngrps = len(new_val.split())
            self.to_write["tau_t"] *= ngrps
            self.to_write["ref_t"] *= ngrps

    def replace_key_val(self, ori_key, new_key, new_val):
        self.to_write = OrderedDict([(new_key, new_val) if k == ori_key else (k, v) for k, v in self.to_write.items()])

    def add_key(self, key, val):
        self.to_write[key] = val

    def add_is(self):
        self.combine([self.to_write, self.implicit_solv])

        self.replace_val("pbc", "no")
        self.replace_val("rcoulomb", "0")
        self.replace_val("rvdw", "0")
    """
    Check the output messages from when running grompp to see which mdp options need to be changed
    """

    def emin(self, implicit_solvent = False):
        self.combine([self.heading, self.run_param, self.neigbours, self.electrostatics])
        self.replace_val("integrator", "steep")
        self.replace_val("nstlist", "1")
        if implicit_solvent:
            self.add_is()
        self.file_name = "emin"

    def nvt(self, implicit_solvent  = False):
        #TODO
        self.combine([self.heading, self.run_param, self.output_control, self.bond_params, self.neigbours, self.electrostatics, self.temp_couple, self.pressure_couple, self.others])
        self.replace_val("pcoupl", "no")
        if implicit_solvent:
            self.add_is()
        self.file_name = "nvt"

    def npt(self, implicit_solvent  = False):
        #TODO
        self.combine([self.heading, self.run_param, self.output_control, self.bond_params, self.neigbours, self.electrostatics, self.temp_couple, self.pressure_couple, self.others])
        self.replace_val("gen_vel", "no")
        if implicit_solvent:
            self.add_is()
        self.file_name = "npt"

    def production(self, implicit_solvent  = False):
        #TODO
        self.combine([self.heading, self.run_param, self.output_control, self.bond_params, self.neigbours, self.electrostatics, self.temp_couple, self.pressure_couple, self.others])
        self.replace_val("gen_vel", "no")
        if implicit_solvent:
            self.add_is()
        self.file_name = "production"

    def pulled(self, implicit_solvent  = False):
        #TODO
        self.combine([self.heading, self.run_param, self.output_control, self.bond_params, self.neigbours, self.electrostatics, self.temp_couple, self.pressure_couple, self.others, self.pull ])
        self.replace_val("gen_vel", "no")
        if implicit_solvent:
            self.add_is()
        self.file_name = "pull"

    def us(self, implicit_solvent  = False):
        #TODO
        if implicit_solvent:
            self.add_is()
        return

    def reset_counter(self): self.counter = 0

    def write(self, file_name = None, postfix = False):
        """
            -Putting equals between key value pair
            -stringfy numbers
        """
        if not file_name:
            file_name = self.file_name

        f = None
        if postfix:
            f = open(file_name + "_" + str(self.counter) + ".mdp", "w")
        else:
            f = open(str(self.counter) + "-" + file_name + ".mdp", "w")

        for i in self.to_write:
            f.write( str(i) + "\t=\t" + str(self.to_write[i]) + "\n")
        f.close()
        self.counter += 1

    heading = OrderedDict([
        ("title", "DEFAULT TITLE"),
        (";define", "-DPOSRES"),
    ])

    run_param = OrderedDict([
        ("integrator", "md"),  # leap-frog integrator
        ("nsteps", "50000"),   # 2 * 50000 = 100 ps
        ("dt", "0.002"),  # 2 fs
        ("emtol", "1000.0"), # Stop minimization when the maximum force < 1000.0 kJ/mol/nm
        ("emstep", "0.01"), #Energy step size
        # Periodic boundary conditions
        ("pbc"         , "xyz"),       # 3-D PBC
    ])

    output_control = OrderedDict([
        ("nstxout"    , 0),       # save coordinates every 1 ps
        ("nstvout"    , 0),       # save velocities every 1 ps
        ("nstxtcout"    , 5000),       # save velocities every 10 ps
        ("nstenergy"  , 5000),       # save energies every 10 ps
        ("nstlog"     , 5000),       # update log file every 10 ps
        #("energygrps" , []),   No longer sure what this does
    ])

    bond_params = OrderedDict([
        ("continuation"    , "no"),            # first dynamics run
        ("constraint_algorithm" , "lincs"),    # holonomic constraints
        ("constraints"     , "all-bonds"),     # all bonds (even heavy atom-H bonds) constrained
        ("lincs_iter"      , 1),             # accuracy of LINCS
        ("lincs_order"     , 4),             # also related to accuracy
    ])


    neigbours = OrderedDict([
        ("ns_type"     , "grid"),      # search neighboring grid cells
        ("nstlist"     , 10),         # 0.002 * 5 = 10 fs
        ("rlist"       , 1.0),       # short-range neighborlist cutoff (in nm)
        ("rcoulomb"    , 1.0),       # short-range electrostatic cutoff (in nm)
        ("rvdw"        , 1.0),       # short-range van der Waals cutoff (in nm)
        ("cutoff-scheme" , "Verlet"),
    ])

    electrostatics = OrderedDict([
        ("coulombtype"     , "PME"),       # Particle Mesh Ewald for long-range electrostatics
        ("pme_order"       , 4),         # cubic interpolation
        ("fourierspacing"  , 0.16),      # grid spacing for FFT
    ])


    temp_couple = OrderedDict([
        ("tcoupl"      , "V-rescale"),                     # modified Berendsen thermostat
        ("tc-grps"     , "System"),# two coupling groups - more accurate
        ("tau_t"       , "0.1 "),                     # time constant, in ps
        ("ref_t"       , "310 "),                    # reference temperature, one for each group, in K

    ])

    pressure_couple = OrderedDict([
        ("pcoupl"      , "Parrinello-Rahman"),             # pressure coupling is on for NPT
        ("pcoupltype"  , "semiisotropic"  ),                   # uniform scaling of box vectors
        ("tau_p"       , "2.0"         ),                  # time constant, in ps
        ("ref_p"       , "1.0 1.0"        ),                   # reference pressure, in bar
        ("compressibility" , "4.5e-5 4.5e-5"),                    # isothermal compressibility of water, bar^-1
        ("refcoord_scaling"    , "com"),
    ])


    others = OrderedDict([
        # Dispersion correction
        ("DispCorr"    , "EnerPres"),  # account for cut-off vdW scheme
        # Velocity generation
        ("gen_vel"     , "yes"),       # assign velocities from Maxwell distribution
        ("gen_temp"    , 310),       # temperature for Maxwell distribution
        ("gen_seed"    , -1),        # generate a random seed
    ])

    implicit_solv = OrderedDict([
        ("implicit_solvent" , "GBSA"),
        ("gb_algorithm"     , "OBC"),
        ("nstgbradii"       , "1"),
        ("rgbradii"         , "1.0"),
        ("gb_epsilon_solvent" , "80"),
        ("gb_dielectric_offset" , "0.009"),
        ("sa_algorithm"         , "Ace-approximation"),
        ("sa_surface_tension"   , "0.0054"),
    ])
    pull = OrderedDict([
        ("pull"              ,     "yes"),
        ("pull_ngroups"    ,       "2"),
        ("pull_ncoords"    ,       "1"),
        ("pull_group1_name"   ,    "DPPC"),
        ("pull_group2_name"      , "Protein"),
        ("pull_coord1_type"       , "umbrella") ,  # harmonic biasing force
        ("pull_coord1_geometry"    ,"direction") ,     # simple distance increase
        ("pull-coord1-vec"     ,   "0 0 -1"),
        ("pull_coord1_groups",     "1 2"),
        ("pull_coord1_dim"     ,   "N N Y"),
        ("pull_coord1_rate"   ,    "0.01") ,         # 0.01 nm per ps = 10 nm per ns
        ("pull_coord1_k"      ,    "3000") ,         # kJ mol^-1 nm^-2
        ("pull_coord1_start" ,     "yes")  ,         # define initial COM distance > 0
   ])
