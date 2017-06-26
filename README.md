# Scripts for Building and Simulating Lipid Systems

## Overview

scripting offers a
great leap in efficiency and more importantly it would significantly reduce the level of random human errors, boosting reliabilities of the final results.


Theses scripts spawn from a molecular dynamics projects studying the interaction between a novel class of polymer - poly(lysine iso-phthalamide) with and without phenylalanine grafted side chains - due to their potentials as drug delivery molecules (experimental study described [here](http://pubs.rsc.org/en/Content/ArticleLanding/2009/JM/b902822f#!divAbstract)).

*Nevertheless,the scripts were written with robustness in mind and have been successfully applied to other simulation projects.*

An important achievement of the project is the construction of force field parameters for different monomer units and defining of rules for concatenating monomers. With such implementation, polymers of various length and compositions can be simulated for further study.


The simulational work utilising these scripts and surronding these polymers are currently under revision for publication. Link to the article will be posted here after publication being accepted.

## Prerequisites
The vast majority of the scripts are written in Python 2.7, non-standard dependencies include `numpy`, `pandas` and `MDAnalysis` libraries, all of which are available via `conda install` or `pip install`.

For R scripts, `ggplot2`, `gridExtra`, `grid`, `ggthemes`, `scales` are needed.

## Directories summary

-  **./analyse**


-  **./config_create**


-  **./plot**

-  **./queue_handle**

-  **./simdir_build**


-  **./topology** *

contains the



## Author

[Shuzhe Wang](linkedin)

## License

This project is licensed under the MIT License
