This is a README for batch_observed_average_Fst_calculator.py

This script takes two inputs

-i = input directory containing the per-site Fst estimates (outputs from vcftools --weir-fst-pop)

-o = the output directory where the output .csv will be printed containing all of the averages 

Note: The script batch_observed_pairwise_Fst_calculator.sh produces inputs for this script

Version changes:

version v2 was updated to properly handle negative Fst values which are treated as 0 

Also updated to strip .weir.fst off the input file names when printed to the output .csv

version v3 was updated to exclude any row with Fst = inf which was causing errors
