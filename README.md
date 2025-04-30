# Fst_bootstrapping_for_assessment_of_groups
Scripts associated with Fst and bootstrapping to assess genetically distinct groups. Used in: Global Characterization of Diversity and Selective Pressures in Five Plasmodium falciparum Loci Identified by Whole-Genome Sieve Analysis as Putative Antigens

Fst_Analysis Process 
#All scripts debugged using AI assistance#

Part 1. Observed Fst values
1.	Prepare files 
  a.	Prepare a VCF for the locus of interest and the samples of interest 
  b.	Prepare input.txt files containing the sample IDs for your groups of interest 
    i.	These could be regions, countries or geographic sites within a country 

2.	Run observed pairwise Fst calculations 
  a.	Scripts: batch_observed_pairwise_Fst_calculator_v2.sh
    i.	-i = input directory containing sample ID files 
    ii.	-o = output directory for all pairwise Fst results 
    iii.	-v = input VCF containing all samples of interest 

3.	Determine Fst averages   
  a.	Scripts: batch_observed_average_Fst_calculator_v2.py
    i.	-i = input directory containing the per-site Fst estimates (output from previous step)
    ii.	-o = output directory for output.csv 

Part 2. Bootstrapping to generate expected Fst values
1.	Enter tmux environment 
  a.	$tmux 

2.	Run bootstrap script
  a.	Script: batch_bootstrap_Fst_average.py 
  b.	-i = input directory containing groups of sample IDs in .txt format (one per line)
  c.	– o = output directory
  d.	-v = input VCF file 

3.	Exit tmux 
  a.	Ctrl + B, press d then enter quickly

4.	Verify session running 
  a.	$tmux list-sessions
  Note: tmux is a work around to nohup / & but more elegant, this opens a session of the terminal that operates like a normal session except is unattached from your login status thus will run in the background until completed  

Part 3. Determining P-values from observed and expected observations
  1.	Run p-value calculator script 
    a.	Script: Fst_pvalue_calculator_v3.py
