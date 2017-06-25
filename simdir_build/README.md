# Overview
These scripts were developed for ease of handling jobs on the supercomputing clusters
(cx1 and cx2 at Imperial College). In order to do so one needs to start with stipulating what a project directory encom-
passes. A project directory is defined to contain only one job submission. This means, a project
has a few stages:

1. preparation for simulation
1. submission for simulation,
1. collection of simulation
1. analysis of results.

If a further round of submission is needed, then it needs to fall within the realm of another project directory.

According to such delegated stages of a project, the directory should contain the following child directories:

- The "Prep" directory is where procedures to generate all the files necessary for a simulation are
kept and executed. Common tasks done here include assembling the overall system from different
pieces of configuration files; extracting windows for USMD from pulling simulation. The directory
contains templates of common tasks need to be run as well as a short system minimisation script
that can be used to test all files needed for a successful GROMACS simulation are present.

- The "Input" directory takes a copy of the end products from the "Prep" directory. Using tools scripts below, commands are generated as a job script (.pbs) which is submitted to the cluster.
As specified in all job scripts, simulation results are always written out to directories starting with

- "Output" (for USMD multiple Output directories exist in a given project).
"Analysis" will contain data and scripts for exploratory analysis and figure generations.

---

# Details

- **MDP_Builder Class**

GROMACS’s molecular dynamics parameter (.mdp) file includes simulation related settings and more using key-value pairs. The MDP_Builder class stores some default values for all the commonly used keys in various or-
dered dictionary data structures. Each ordered dictionary stores a group of settings, for example, all the parameters for pull-simulation to get umbrella sampling windows are stored in the same ordered dictionary. When the write() method is called, the relevant ordered dictionaries are collected and a .mdp file is generated with all these selected key-value pairs.
Templates for assembling the right sets of ordered dictionaries for common MD simulations tasks are defined in the class. Additionally, object methods exist in the class for adding, deleting key-value pairs, or modifying values for a given key. The class has a counter that assigns an ascending number to the file name of the produced
.mdp files (number as postfix for replica exchange and prefix for other cases). This is important for the PBS_Builder class below.



---

- **PBS_Builder Class**

Generates .pbs type job files for cx1/cx2. It parses through files in the
input directory looking for all the .mdp files. Based on the number ordering, PBS_Builder collates the first .mdp, the .top, .gro and other optional files for the GROMACS Pre-Process (grompp) method to produce binary file ready for simulation (.tpr). It then uses the out-
puts from this simulation (assuming it ran successfully) for further simulation using the next .mdp file.
Two classes inherit from PBS_Builder, namely **US_PBS_Builder** and **RE_PBS_Builder** for umbrella sampling set-ups and replica exchange set-ups. The former handles creation of multiple .pbs files, one fore each window along the reaction coordinate, which all shares the
same topology (.top) file and MD parameters (.mdp) file, but have different configuration (.gro) files. The latter creates a single .pbs file which uses different .mdp files (temperature variation) but the same topology and starting configurations.

---

- **simdir**

Create a simulation directory at the location where this script is called. The argument following simdir is taken as the directory name. Inside the created directory, "Input" and "Prep" directories (stored in `DIR_CONSTRUCT`) are created and the force field parameter files are deposited into them.
