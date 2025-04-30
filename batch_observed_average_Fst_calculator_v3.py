import os
import csv
import argparse
import numpy as np

def parse_fst_file(file_path):
    fst_values = []
    with open(file_path, 'r') as file:
        next(file)  # Skip header
        for line in file:
            fields = line.strip().split()
            try:
                fst_value = float(fields[2])
                if not np.isnan(fst_value) and not np.isinf(fst_value):
                    fst_values.append(max(0, fst_value))
                elif np.isinf(fst_value):
                    print(f"Excluding infinite FST value: {fst_value}")
            except ValueError as e:
                print(f"Error parsing line '{line}': {e}")

    if fst_values:
        summed_fst_values = sum(fst_values)
        length_fst_values = len(fst_values)
        average_fst = summed_fst_values / length_fst_values
        print(f"Summed FST values: {summed_fst_values}")
        print(f"Number of FST values used: {length_fst_values}")
        return average_fst
    else:
        return 0.0

def main(input_dir, output_dir):
    output_rows = []
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.weir.fst'):
            file_path = os.path.join(input_dir, file_name)
            average_fst = parse_fst_file(file_path)
            # Remove ".weir.fst" extension from file name
            file_name_without_extension = file_name.replace('.weir.fst', '')
            output_rows.append([file_name_without_extension, average_fst])

    output_file = os.path.join(output_dir, 'Observed_Fst_averages.csv')
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File Name', 'Average FST'])
        writer.writerows(output_rows)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate average FST values from .weir.fst files')
    parser.add_argument('-i', '--input_dir', type=str, help='Input directory containing .weir.fst files', required=True)
    parser.add_argument('-o', '--output_dir', type=str, help='Output directory for the CSV file', required=True)
    args = parser.parse_args()

    main(args.input_dir, args.output_dir)

