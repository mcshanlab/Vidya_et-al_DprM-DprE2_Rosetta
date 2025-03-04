# written by andrew mcshan
# simple script to run rosetta calculations and scripts to filter results
# to run do ./idealize_relax_score_part2.sh

# idealize bonds to minimize xtal structure
# idealizing means bond lengths and angles will be their “ideal” state
#idealize_jd2.static.macosclangrelease -s DprM-DprE2_WT.pdb

# remove idealized score file
#rm score.sc

# relax side-chain rotamers to minimize xtal structure but keep overall structure roughly same
# relaxing means sampling most energetically favorable conformation in your protein
#relax.static.macosclangrelease -s *_0001.pdb -use_input_sc -constrain_relax_to_start_coords -nstruct 1 -relax:coord_constrain_sidechains -relax:ramp_constraints false -relax:cartesian -relax:min_type lbfgs_armijo_nonmonotone -score:set_weights pro_close 0 cart_bonded 0.5

# make mutation Y437H and calculate ddG using rosetta's cartesian_ddg function
# mutation list numbering is weird since rosetta's pose starts from 1
cartesian_ddg.static.macosclangrelease -s *_0001_0001.pdb -ddg:mut_file mutation_list.txt -ddg:iterations 1 -optimization:default_max_cycles 200 -ddg:bbnbrs 1 -relax:min_type lbfgs_armijo_nonmonotone -fa_max_dis 9.0 -score:set_weights pro_close 0 cart_bonded 0.5 -ddg::dump_pdbs true

#run the analysis script to get the difference in MUT - WT values
# lower values = mutation makes it better, higher values = mutation makes it worse
python3 calculate_ddG_rosetta-parameters.py
