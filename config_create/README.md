
- **shift**

Moves the coordinates in the configuration along the direction "-d" by an amount specified after "-s". The periodic boundary box size is kept unchanged.

---

- **stack**

Concatenates two .gro type GROMACS configuration files with path specified after "-f" and "-g" flags. Argument after "-d" flag sets the direction that the two configurations are stacked with, default it "z" (one is put on top of the other). "s" sets a distance of separation between the two, default is 0.


---


- **flip**

Inverts the direction along the coordinate axis specified after flag "-d".

---

- **expand**

Replicates the configuration along the direction specified after "-d" a number of times (specified after "r") with distance of separation between replicas specified after "-s", default is 0.

---

- **topol**

Tallies and outputs the molecular ordering in the given configuration files. The corrected ordering is needed in the "[ molecules ]" section in the .top GROMACS topology files.

---

- **pick_frame**

Given a pulled simulation trajectory along a reaction coordinate, it selects simulation windows at regular distance of separation between the two pulled groups (default 0.2 nm).

---

- **transformations.py**

A set of functions written by Christoph Gohlke that are mainly used to rotate and rescale difference configurations.
