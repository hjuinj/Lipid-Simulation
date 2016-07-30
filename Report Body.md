
<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [BACKGROUND](#background)
	- [1. The Biology](#1-the-biology)
	- [2. MD: Theoretical Framework](#2-md-theoretical-framework)
	- [3. Computational Tool : Gromacs](#3-computational-tool-gromacs)
		- [1. Useful commands](#1-useful-commands)
- [OBJECTIVES](#objectives)

<!-- /TOC -->

# BACKGROUND

## 1. The Biology

## 2. MD: Theoretical Framework

## 3. Computational Tool : Gromacs
Applying temperature and pressure coupling separately to  to the different types of molecules in the system
### 1. Useful commands
itp file: include topology type file, included in the system topology file contains atom type and bonding/non-bonding interaction parameters

top file contains the atom indexed, bonding pairs, pairs, angle trios and dihedrial quartet
- pdb2gmx : creates corodinates and topology file for use, -ignh ignores hydrogen, -water water model, -ff forcefield -f file -o output, it turns a pdb file into a gro, itp and top file.
- editconf -bt box type -d spacing distance in nm
- grompp gromacs preprocessor,

Two step equilibration   

# OBJECTIVES
- Scripting
- Sampling technique
