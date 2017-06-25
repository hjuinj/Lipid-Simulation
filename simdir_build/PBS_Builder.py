#!/usr/bin/env python
import os
import shutil
import numpy as np
import textwrap
import re

"""
TODOs:
    - TESTING: the ability to run multiple .mdp files in one go


    - directories should be os.var.abspath() treated to avoid macros causing issues

    - Account for the job title field - needs more specificity
    - Ensure the number of stages is capatible with the number of mdp files available
    - US: how are output folders named
    - Energy minimisation step?
    - Ignore all #...# type files?

    - US: Strategy for writing the pbs files to different directories (solved)
"""

"""
- The script name appearing in the q (obtained from the pbs file) can be a maximum of 16 characters long
"""

class PBS_Builder(object):
    template = """
    #!/bin/sh

    #PBS -l walltime=71:59:00
    #PBS -l select=1:ncpus=DEFAULT_CPUS
    #PBS -N DEFAULT_TITLE

    module load intel-suite
    module load mpi/intel-5.0
    module load anaconda/2.4.1
    module load gromacs/5.1.4

    rm *tpr
    cp -r $PBS_O_WORKDIR/Input/* $TMPDIR
    mkdir $PBS_O_WORKDIR/DEFAULT_OUTPUT
    cd $TMPDIR

    DEFAULT_COMMANDS

    mv $TMPDIR/* $PBS_O_WORKDIR/DEFAULT_OUTPUT

    python $HOME/Scripts/remove_duplicate_files.py $PBS_O_WORKDIR/Input $PBS_O_WORKDIR/DEFAULT_OUTPUT
    """

    template_cx2 = """
    #!/bin/sh

    #PBS -l walltime=71:59:00
    #PBS -l select=DEFAULT_NODES:ncpus=DEFAULT_CPUS:mpiprocs=DEFAULT_PROCS:mem=2000mb

    #PBS -N DEFAULT_TITLE

    module load intel-suite/11.1
    module load mpi
    module load anaconda/2.4.1
    module load gromacs/4.5.5

    rm *tpr
    TMPDIR=$PBS_O_WORKDIR/DEFAULT_OUTPUT
    mkdir $TMPDIR
    cp -r $PBS_O_WORKDIR/Input/* $TMPDIR
    cd $TMPDIR

    DEFAULT_COMMANDS

    python $HOME/Scripts/remove_duplicate_files.py $PBS_O_WORKDIR/Input $PBS_O_WORKDIR/DEFAULT_OUTPUT
    """
    def __init__(self, stages = 1, output_dir = "Output", cx2 = False, title = "GRO_SIM", nodes = "1", cpus  = "20", dir = "./", emin_pattern = "min.mdp"):
        """
        the script will process things in the input file
        """
        #self.template = self.template.replace("DEFAULT_COMMANDS", commands)
        self.title = (title + " " * 15)[ : 15]
        self.cpus = cpus
        self.output_dir = output_dir
        self.dir = dir
        self.emin_pattern = emin_pattern
        self.include_cpt = False
        # self.commands = []
        self.stages = stages
        self.previous_simulation = None
        self.current_stage = 0
        self.nodes = nodes
        if cx2:
            self.template = self.template_cx2
            self.nodes = "36"

    def set_title(self, new_title): self.title = str(new_title)[ : 15]
    def set_cpus(self, new_cpus): self.cpus = str(new_cpus)
    def set_nodes(self, new_nodes): self.nodes = str(new_nodes)
    def set_output_dir(self, new_output_dir): self.output_dir = new_output_dir

    def simple_check(self, dir = None):
        if dir is None:
            dir = self.dir
        output = [i.split(".")[-1] for i in os.listdir(dir)]
        print "number of .mdp files: %d\nnumber of .ndx files: %d\nnumber of .top files: %d" %(output.count("mdp"), output.count("ndx"), output.count("top"))

    def make_tpr(self, cfg, mpi = False, dir = None):
        if dir is None:
            dir = self.dir
        if self.current_stage == 0:
            cmd = "gmx grompp -c %s" %(cfg)
            for f in os.listdir(dir):
                if os.path.isdir(f):
                    continue
                if f.endswith(".top"):
                    cmd += (" -p " + f)
                elif f.endswith(".ndx"):
                    cmd += (" -n " + f)
                elif f.endswith(".cpt"): # Allows inclusion of cpt file
                    cmd += (" -t " + f)
                elif f.startswith("0-") and f.endswith(".mdp") and f != "mdout.mdp":
                    cmd += (" -f " + f + " -o " + f[2:-4] + ".tpr")  # the tpr has the same name as the mdp file without the starting numbering
                    if self.emin_pattern in f:
                        self.include_cpt = False
                    else: self.include_cpt = True
                    self.previous_simulation = f[2:-4]
        else:
            cmd = "gmx grompp -c %s " %(self.previous_simulation + ".gro")  #TODO allow g96 format???

            if self.include_cpt:
                cmd += (" -t " + self.previous_simulation + ".cpt")

            for f in os.listdir(dir):
                if f.endswith(".top"):
                    cmd += (" -p " + f)
                elif f.endswith(".ndx"):
                    cmd += (" -n " + f)
                elif f.startswith(str(self.current_stage) + "-") and f.endswith(".mdp") and f != "mdout.mdp":
                    cmd += (" -f " + f + " -o " + f[2:-4] + ".tpr")  # the tpr has the same name as the mdp file without the starting numbering
                    if self.emin_pattern in f:
                        self.include_cpt = False
                    else: self.include_cpt = True

                    self.previous_simulation = f[2:-4]
        self.current_stage += 1
        if mpi:
            cmd = cmd.replace("gmx ", "gmx_mpi ")
        return cmd


    def make_mdrun(self, mpi = False, extra_args = ""):
        cmd = "gmx mdrun -deffnm %s %s" %(self.previous_simulation, extra_args)
        cmd += " -nt %d -ntomp %d" %(self.cpus, self.cpus)
        if mpi:
            cmd = cmd.replace("gmx ", "gmx_mpi ")
        #self.commands.append(cmd)
        return cmd

    def make_mdrun4mpi(self, **kwargs):
        return "pbsexec mpiexec " + self.make_mdrun(**kwargs)

    def make_commands(self, init_config, **kwargs):
        # return "\n".join(self.commands)
        self.commands = []
        for i in range(self.stages):
            # self.commands += [ self.make_tpr(init_config), self.make_mdrun4mpi(**kwargs), ""]
            self.commands += [ self.make_tpr(init_config), self.make_mdrun(**kwargs), ""]
        return "\n".join(self.commands)

    #def add_commands(self):
    #    self.template = self.template.replace("DEFAULT_COMMANDS", self.make_commands())

    def write_pbs(self, init_config, file_name = "job.pbs", dir = None, **kwargs):
        if dir is None:
            dir = self.dir
        else:
            self.dir = dir
        self.template = self.template.replace("DEFAULT_OUTPUT", self.output_dir)
        self.template = self.template.replace("DEFAULT_CPUS", self.cpus)
        self.template = self.template.replace("DEFAULT_NODES", self.nodes)
        self.template = self.template.replace("DEFAULT_TITLE", self.title)
        self.template = textwrap.dedent(self.template)
        self.template = self.template.replace("DEFAULT_COMMANDS", self.make_commands(init_config, **kwargs))
        f = open(dir + file_name, "w")
        self.pbs_location = dir + file_name
        f.write(self.template)
        f.close()

class US_PBS_Builder(PBS_Builder):
    """
    Basically builds multiple PBS files in one go
    """
    # def __init__(self, frames, title = "null", cpus  = "20"):
    #     self.frames = frames
    #     super(US_PBS_Builder, self).__init__(title, cpus)
    def select_frames_helper(self, end, frames, start = 0):
        # step = (start + end) / float(frames - 1)
        step = (end - start) / float(frames - 1)
        result = []
        for i in range(frames):
            result.append(start)
            start += step
        return [int(i) for i in result]

    def make_mdrun(self, mpi = False, extra_args = ""):
        cmd = "gmx mdrun -deffnm %s %s" %(self.previous_simulation, extra_args)
        cmd += " -nt %s -ntomp %s" %(self.cpus[self.counter], self.cpus[self.counter])
        if mpi:
            cmd = cmd.replace("gmx ", "gmx_mpi ")
        #self.commands.append(cmd)
        return cmd
    def select_frames(self, frames = -1 , pattern = "conf#.gro", dir = None, start = None, end = None):
        """
        frames = -1 means no need to work out which frames to take, just take all the ones listed in current directory

        replaces a hash # with a number
        """
        if dir is None:
            dir = self.dir
        self.pattern = pattern
        pat = re.compile(pattern.replace("#", "[0-9]+"))
        files = []
        for file in os.listdir(dir):
            if pat.match(file) != None:
                files.append(int(filter(str.isdigit, file)))

        if frames == -1:
            self.frames = files
        elif start == None and end == None:
            start, end, self.frames = min(files), max(files), frames
            self.frames = self.select_frames_helper(end, frames, start)
        else:
            self.frames = self.select_frames_helper(end, frames, start)
        #self.frames = [pattern.replace("#", str(i)) for i in self.frames]
        self.title = [("f" + str(i))[ : 15] for i in self.frames]
        self.output_dir = ["Output_frame" + str(i) for i in self.frames]
        self.cpus = [self.cpus] * len(self.frames)
        self.template = [self.template] * len(self.frames)

        #print self.frames

    # def select_frame(self, frame_name, dir = "./", **kwargs):
    #     """
    #     Wrapper around the make_commands method in the parent function
    #     """
    #     self.make_commands(frame_name, **kwargs)

    def make_us_commands(self, **kwargs):
        output = []
        for idx,val in enumerate([self.pattern.replace("#", str(i)) for i in self.frames]):
            self.counter = idx
        #    print self.make_commands(i)
            output.append(self.make_commands(val, extra_args = "-pf pullf.xvg -px pullx.xvg"))
            self.current_stage = 0
        return output

    def set_cpus(self, cpu_idx, cpu_val):
        """
        supply lists as arguments
        """

        for i in xrange(len(cpu_idx)):
            self.cpus[cpu_idx[i]] = str(cpu_val[i])

    def set_titles(self, title_idx, title_val):
        for i in xrange(len(title_idx)):
            self.title[cpu_title[i]] = title_val[i]

    def write_us_pbs(self, file_name_pattern = "frame#.pbs", dir = None, **kwargs):
        self.pbs_objs = []
        self.pbs_locations = []
        if dir is None:
            dir = self.dir
        else:
            self.dir = dir
        cmds = self.make_us_commands(**kwargs)
        for idx, val in enumerate(self.frames):
            self.template[idx] = self.template[idx].replace("DEFAULT_OUTPUT", self.output_dir[idx])
            self.template[idx] = self.template[idx].replace("DEFAULT_TITLE", self.title[idx])
            self.template[idx] = self.template[idx].replace("DEFAULT_CPUS", self.cpus[idx])
            self.template[idx] = textwrap.dedent(self.template[idx])
            self.template[idx] = self.template[idx].replace("DEFAULT_COMMANDS", cmds[idx])

            f = open(dir + file_name_pattern.replace("#", str(val)), "w")
            self.pbs_locations.append(dir + file_name_pattern.replace("#", str(val)))
            f.write(self.template[idx])
            f.close()

            # how useful is this line?
            self.pbs_objs.append(PBS_Builder(self.stages, self.output_dir[idx], self.title[idx], self.cpus[idx], self.dir))

class RE_PBS_Builder(PBS_Builder):
    """
    Writes one PBS file with a lot more commands in it
    """
    def __init__(self, num_simulations, stages = 1, output_dir = "Output", cx2 = True, title = "GRO_SIM", nodes = "36", cpus  = "24", procs = "24", dir = "./", emin_pattern = "min.mdp"):
        super(RE_PBS_Builder, self).__init__(stages, output_dir, cx2, title, nodes, cpus, dir, emin_pattern)
        self.num_simulations = num_simulations
        self.previous_simulation = [None] * num_simulations
        self.cmds = ""
        self.nodes = num_simulations

    def make_tpr(self, mdp, cfg = "init", mpi = False, dir = None):
        if dir is None:
            dir = self.dir
        cmd = ""
        for sim in range(self.num_simulations):
            if self.current_stage == 0:
                # cmd += "gmx grompp -c %s" %(cfg + "_" + str(sim) + ".gro")
                cmd += "grompp -c %s" %(cfg + "_" + str(sim) + ".gro")
                for f in os.listdir(dir):
                    if os.path.isdir(f):
                        continue
                    if f.endswith(".top"):
                        cmd += (" -p " + f)
                    elif f.endswith(".ndx"):
                        cmd += (" -n " + f)
                    elif f.endswith(".cpt"): # Allows inclusion of cpt file
                        cmd += (" -t " + f)
                    elif f.startswith(mdp + "_" + str(sim) + ".") and f.endswith(".mdp"):
                        cmd += (" -f " + f + " -o " + f[0:-4] + ".tpr")  # the tpr has the same name as the mdp file without the starting numbering
                        if self.emin_pattern in f:
                            self.include_cpt = False
                        else: self.include_cpt = True
                        self.previous_simulation[sim] = f[0:-4]
            else:
                # cmd += "gmx grompp -c %s " %(self.previous_simulation[sim] + ".gro")  #TODO allow g96 format???
                cmd += "grompp -c %s " %(self.previous_simulation[sim] + ".gro")  #TODO allow g96 format???
                if self.include_cpt:
                    cmd += (" -t " + self.previous_simulation[sim] + ".cpt")
                for f in os.listdir(dir):
                    if f.endswith(".top"):
                        cmd += (" -p " + f)
                    elif f.endswith(".ndx"):
                        cmd += (" -n " + f)
                    elif f.startswith(mdp + "_" + str(sim) + ".") and f.endswith(".mdp"):
                        cmd += (" -f " + f + " -o " + f[0:-4] + ".tpr")  # the tpr has the same name as the mdp file without the starting numbering
                        if self.emin_pattern in f:
                            self.include_cpt = False
                        else: self.include_cpt = True
                        self.previous_simulation[sim] = f[0:-4]
            # cmd += "\n sleep 5s \n"
            cmd += "\n \n"
        if mpi:
            cmd = cmd.replace("gmx ", "gmx_mpi ")
        self.current_stage += 1
        self.cmds += cmd
    def set_procs(self, new_procs): self.procs = str(new_procs)

    def make_cmds(self, mdp, cfg = "init", replex = None, extra_args = ""):
        self.make_tpr(mdp, cfg)
        # cmd = "pbsexec mpiexec gmx_mpi mdrun -deffnm %s -multi %s" %(self.previous_simulation[0][:-1], self.num_simulations)
        cmd = "pbsexec mpiexec mdrun -deffnm %s -multi %s -maxwarn 2" %(self.previous_simulation[0][:-1], self.num_simulations)
        if replex:
            cmd += " -replex " + str(replex)
        # self.cmds += cmd + "\n sleep 5s \n" + "\n"
        self.cmds += cmd + "\n \n" + "rm \#*" + "\n \n \n"


    def write_re_pbs(self, file_name = "job.pbs", dir = None, **kwargs):
        if dir is None:
            dir = self.dir
        else:
            self.dir = dir
        self.template = self.template.replace("DEFAULT_OUTPUT", self.output_dir)
        self.template = self.template.replace("DEFAULT_CPUS", self.cpus)
        self.template = self.template.replace("DEFAULT_NODES", self.nodes)
        self.template = self.template.replace("DEFAULT_PROCS", self.procs)
        self.template = self.template.replace("DEFAULT_TITLE", self.title)
        self.template = textwrap.dedent(self.template)
        self.template = self.template.replace("DEFAULT_COMMANDS", self.cmds)
        f = open(dir + file_name, "w")
        self.pbs_location = dir + file_name
        f.write(self.template)
        f.close()
    # def get_frames(self, frames = -1 , pattern = "conf#.gro", dir = None ):
    #     """
    #     frames = -1 means no need to work out which frames to take, just take all the ones listed in current directory
    #
    #     replaces a hash # with a number
    #     """
    #     if dir is None:
    #         dir = self.dir
    #     self.pattern = pattern
    #     pat = re.compile(pattern.replace("#", "[0-9]+"))
    #     files = []
    #     for file in os.listdir(dir):
    #         if pat.match(file) != None:
    #             files.append(int(filter(str.isdigit, file)))
    #     self.frames = files
    #     self.previous_simulation = {}



# def order_frames(self):
#     """
#     Order by prioritising frames that are most distant from frames that have been selected in the past
#     """
#     assert(len(self.frames) > 1)
#     result = [self.frames.pop(0), self.frames.pop(-1)]
#     while len(self.frames) > 0:
#         max_dis = -1
#         which = -1
#         for i in self.frames:
#             tmp = sum(abs(np.array(result) - i))
#             if tmp > max_dis:
#                 max_dis = tmp
#                 which = i
#         self.frames.remove(i)
#         result.append(i)
#     self.frames = result

# us = US_PBS_Builder(dir = "../7week/4day/")
# #us.select_frames(20, pattern = "conf#.gro",  dir = "/home/shuzhe/Sandbox/build/insert/simulation/frames")
# us.select_frames(20, pattern = "conf#.gro")
# #x = us.make_us_commands(dir = "../")
# us.write_us_pbs()
#
# pbs = PBS_Builder(2)
#pbs.make_tpr("./npt.gro")
#pbs.make_mdrun()
# pbs.write_pbs("/home/shuzhe/Simulations/9week/1.PP75-1_dppc128_sysprep/Input/combined.gro")
# pbs.write_pbs("./npt.gro")
