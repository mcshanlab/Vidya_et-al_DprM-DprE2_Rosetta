#!/bin/bash

pose="DprM-DprE2_WT_0001_0001.pdb"

for chain in B; do
    for seqpos in 1 2 3 4 5 6 7 8 9 10 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86; do
    # site 1 = 1 - 10
    # site 2 = 72 - 86
	for aa in ALA ARG ASN ASP GLU GLN GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL; do
	    rosetta_scripts.static.macosclangrelease -s $pose -parser:protocol point_mutant_scan.xml -parser:script_vars focused_res=$seqpos focused_chain=$chain target_aa=$aa -out:prefix ${chain}${seqpos}_${aa}
	done
    done
done
