:<<'comment'
### US command
gmx trjconv -s pull.tpr -f pull.xtc -o conf.gro -sep << EOF 
0
EOF
rm ./Input/conf*.gro
file="frames"
if [ -f "$file" ]
then
	while read -r line
	do
	     echo Moved conf"$line".gro to Input
	     cp conf"$line".gro ../Input
	done < "$file"
else
	echo Select frames, press ctr-D to exit:
	while read line
	do
	     echo Moved conf"$line".gro to Input
	     cp conf"$line".gro ../Input
	done
fi

rm conf*.gro

###
gmx pdb2gmx -f input.pdb -inter -missing
gmx make_ndx -f input.gro

### Join peptide with lipid system together
SysPrep -l lipid.gro -p peptide.gro -o ./combined.gro --solvate #toggle betwen solvate/combine
mv combined.gro ../Input/init.gro

### Solvating system
gmx editconf -f PP75_monomer_OH.gro -bt cubic -box 3 3 3
gmx solvate -p topol.top -cp out.gro  -cs spc216.gro -o PP75-1_solv.gro
cp PP75-1_solv.gro ../Input/init.gro



### Generic Housekeeping
cp topol.top ../Input/
cp *.ndx ../Input/
cp *.itp ../Input/
rm out.gro
rm \#*\#
comment
