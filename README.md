# Scripts for Building and Simulating Lipid Systems

## Overview

This repo contains different sets of scripts used for molecular dynamics simulation using [GROMACS](www.gromacs.org) that aim to automate various stages of a simulation project, such as building the initial configurations, analysing the simulation outcomes and handling the simulation queue when large number of simulations have been submitted. These scripts offer a great leap in efficiency and significantly reduction in the level of random human errors, boosting reliabilities of the final results. The ultimate goal is to build a complete pipeline of automation scripts which would allow highthroughput molecular dynamics (HTMD) be carried out. This means a large number of parallel studies, with minor configurational or simulating condition differences, can be easily simulated at once.

Theses scripts spawn from a molecular dynamics projects studying the interaction between lipid bilayer and a novel class of polymer - poly(lysine iso-phthalamide) with and without phenylalanine grafted side chains - due to their potentials as drug delivery molecules (experimental study described [here](http://pubs.rsc.org/en/Content/ArticleLanding/2009/JM/b902822f#!divAbstract)).

*Nevertheless,the scripts were written with robustness in mind and have been successfully applied to other simulation projects.*

Another important achievement of the project is the construction of force field parameters for different monomer units and defining of rules for concatenating monomers. With such implementation, polymers of various length and compositions can be simulated for further study.


The simulational work utilising these scripts and surronding these polymers are currently under revision for publication. Link to the article will be posted here after publication being accepted.

## Prerequisites
The vast majority of the scripts are written in Python 2.7, non-standard dependencies include `numpy`, `pandas` and `MDAnalysis` libraries, all of which are available via `conda install` or `pip install`.

For R scripts, `ggplot2`, `gridExtra`, `grid`, `ggthemes`, `scales` are needed.

## Directories summary

-  **./analyse**

Contains scripts to analyse simulation trajectories, including lipid specific properties such as tilt angle, average thickness, as well as other more generic properties such as radial distribution function, radius of gyration and also example Markov State Model (MSM) notebook for finding correlation time and stable conformations.

-  **./config_create**

Contains scripts to manipulate configurations to be submitted for simulation, including putting together and replicating different simulation blocks as well as picking frames from a simulation trajectory in order to to umbrella sampling.


-  **./plot**

Contains R scripts to plot results such as potential of mean force path, radius of gyration distributions.

-  **./queue_handle**

Contains scripts to monitor high performance cluster queue and handle jobs in queues.

-  **./simdir_build**

Contains scripts to build simulation directories with automated construction of the various file formats required by GROMACS for simulation including generating files needed for advanced sampling simulations such as umbrella sampling and replica exchange molecular dynamics.

---

-  **./topology** *

*Contains the force field parameters for the monomer units of the polymer studied as well as script to concatenate monomers to form polymers.*

---

## Author

[Shuzhe Wang](linkedin)

## License

This project is licensed under the MIT License
