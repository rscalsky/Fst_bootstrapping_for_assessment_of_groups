#!/bin/bash

# Function to display usage message
usage() {
  echo "Usage: $0 -i input_directory -o output_directory -v input_vcf"
  exit 1
}

# Parse command-line options
while getopts ":i:o:v:" opt; do
  case ${opt} in
    i )
      pop_dir=$OPTARG
      ;;
    o )
      output_dir=$OPTARG
      ;;
    v )
      input_vcf=$OPTARG
      ;;
    \? )
      usage
      ;;
    : )
      usage
      ;;
  esac
done

# Check if all options are provided
if [ -z "$pop_dir" ] || [ -z "$output_dir" ] || [ -z "$input_vcf" ]; then
  usage
fi

# Check if the input directory exists
if [ ! -d "$pop_dir" ]; then
  echo "Input directory $pop_dir does not exist."
  exit 1
fi

# Check if the input VCF file exists
if [ ! -f "$input_vcf" ]; then
  echo "Input VCF file $input_vcf does not exist."
  exit 1
fi

# Print input and output directories and input VCF for debugging
echo "Input directory: $pop_dir"
echo "Output directory: $output_dir"
echo "Input VCF: $input_vcf"

# Create the output directory if it does not exist
mkdir -p "$output_dir"

# Array to hold the population files
pop_files=($(ls ${pop_dir}/*.txt))

# Check if pop_files array is empty
if [ ${#pop_files[@]} -eq 0 ]; then
  echo "No .txt files found in the input directory."
  exit 1
fi

# Get the number of population files
num_files=${#pop_files[@]}

# Loop through each unique pair of population files
for (( i=0; i<$num_files; i++ )); do
  for (( j=i+1; j<$num_files; j++ )); do
    pop1=${pop_files[$i]}
    pop2=${pop_files[$j]}

    # Extract the base names without the directory and the "_sample_IDs.txt" suffix
    base1=$(basename "$pop1" _sample_IDs.txt)
    base2=$(basename "$pop2" _sample_IDs.txt)

    # Define the output file name
    output_file="${output_dir}/${base1}_vs_${base2}.txt"

    # Run the vcftools command
    vcftools --vcf "$input_vcf" --weir-fst-pop "$pop1" --weir-fst-pop "$pop2" --out "${output_file%.txt}"
  done
done

