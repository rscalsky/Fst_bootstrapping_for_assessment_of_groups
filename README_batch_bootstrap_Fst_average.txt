This is a README for batch_bootstrap_Fst_average.py 

This script will take three user command options 

-i = directory containing country_sample_IDs.txt

-o = out directory where all .csv outputs will be saved

-v = input.vcf containing all samples

This script will evaluate all of the unique pairs of countries within the -i directory and perform the following on them 1000 times: 

1) Combine subject IDs from both and randomly assign subject IDs to two temporary files of the same sample size as the originals
2) Run vcftools Fst estimates on the simulated samples 
3) Average the Fst where -nan are not considered and negative (-) values are considered 0 
4) print the simulated run number (i.e. iteration of the 1000 loop) and average Fst to an output.csv named accordingly

Notes: country_sample_IDs.txt files are identified by any .txt file in the -i input directory 


version 2 adjusted so that ay vcftools output with Fst = inf is removed before averages are calculated - prevents Fst average = inf
