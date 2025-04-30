import os
import random
import subprocess
import numpy as np
import argparse

print(os.getcwd())

# Function to read sample IDs from a file
def read_sample_ids(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Function to write sample IDs to a file
def write_sample_ids(file_path, sample_ids):
    with open(file_path, 'w') as file:
        for sample_id in sample_ids:
            file.write(f"{sample_id}\n")

# Function to calculate average Fst from vcftools output
def calculate_average_fst(output_file):
    fst_values = []
    try:
        with open(output_file, 'r') as file:
            next(file)  # skip header
            for line in file:
                _, _, fst = line.split()
                if fst != "-nan" and fst != "inf":
                    fst_value = max(float(fst), 0.0)
                    fst_values.append(fst_value)
    except FileNotFoundError:
        print(f"Error: {output_file} not found.")
    return np.mean(fst_values) if fst_values else 0

# Main script logic
def main(input_dir, output_dir, input_vcf):
    # Check if input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return

    # Check if output directory exists, if not create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get list of sample ID files
    sample_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]

    # Print the found sample files for debugging purposes
    print("Sample ID files found:")
    for sample_file in sample_files:
        print(sample_file)

    pairs = [(sample_files[i], sample_files[j]) for i in range(len(sample_files)) for j in range(i+1, len(sample_files))]

    # Print the unique pairs array for debugging purposes
    print("Unique pairs of subject ID files:")
    for pair in pairs:
        print(pair)

    # If no pairs found, exit
    if not pairs:
        print("No pairs of subject ID files found. Exiting.")
        return

    # Process each pair of sample files
    for file1, file2 in pairs:
        sample_ids1 = read_sample_ids(os.path.join(input_dir, file1))
        sample_ids2 = read_sample_ids(os.path.join(input_dir, file2))

        # Create base name by removing '_subject_IDs.txt' and adding '_vs_' between file names
        base_name1 = file1.replace('_sample_IDs.txt', '')
        base_name2 = file2.replace('_sample_IDs.txt', '')
        base_name = f"{base_name1}_vs_{base_name2}"

        output_csv = os.path.join(output_dir, f"{base_name}_Simulated_Fst.csv")

        # Prepare the output CSV file
        with open(output_csv, 'w') as out_csv:
            out_csv.write("simulated_run,simulated_Fst_averages\n")

        # Run simulations
        for sim_num in range(1, 1001):
            combined_ids = sample_ids1 + sample_ids2
            random.shuffle(combined_ids)

            sim_pop1 = combined_ids[:len(sample_ids1)]
            sim_pop2 = combined_ids[len(sample_ids1):]

            temp_pop1_file = f"temp_pop1_{sim_num}.txt"
            temp_pop2_file = f"temp_pop2_{sim_num}.txt"
            write_sample_ids(temp_pop1_file, sim_pop1)
            write_sample_ids(temp_pop2_file, sim_pop2)

            output_prefix = f"temp_output_{sim_num}"
            vcftools_cmd = [
                "vcftools",
                "--vcf", input_vcf,
                "--weir-fst-pop", temp_pop1_file,
                "--weir-fst-pop", temp_pop2_file,
                "--out", output_prefix
            ]

            # Print vcftools command for debugging
            print(f"Running vcftools command: {' '.join(vcftools_cmd)}")

            # Run vcftools command and check for errors
            try:
                subprocess.run(vcftools_cmd, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error running vcftools: {e}")
                continue

            fst_file = f"{output_prefix}.weir.fst"
            avg_fst = calculate_average_fst(fst_file)

            with open(output_csv, 'a') as out_csv:
                run_name = f"{base_name}_sim_{sim_num}"
                out_csv.write(f"{run_name},{avg_fst}\n")

            # Clean up temporary files
            os.remove(temp_pop1_file)
            os.remove(temp_pop2_file)
            os.remove(f"{output_prefix}.log")
            os.remove(f"{output_prefix}.weir.fst")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bootstrap Fst calculations using vcftools.")
    parser.add_argument("-i", required=True, help="Directory containing subject ID .txt files")
    parser.add_argument("-o", required=True, help="Output directory for .csv outputs")
    parser.add_argument("-v", required=True, help="Input VCF file")

    args = parser.parse_args()
    main(args.i, args.o, args.v)

