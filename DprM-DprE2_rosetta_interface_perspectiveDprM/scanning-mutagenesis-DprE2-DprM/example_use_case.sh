#!/bin/bash

pose="DprM-DprE2_WT_0001_0001.pdb"

for chain in A; do
    for seqpos in 201 202 203 204 205 206 207 208 209; do
    #for seqpos in 49; do
	for aa in ALA ARG ASN ASP GLU GLN GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL; do
	    rosetta_scripts.static.macosclangrelease -s $pose -parser:protocol point_mutant_scan.xml -parser:script_vars focused_res=$seqpos focused_chain=$chain target_aa=$aa -out:prefix ${chain}${seqpos}_${aa}
	done
    done
done

# -nstruct 5
