import os
import pandas as pd
import numpy as np
import argparse

def calculate_p_value(observed_fst, simulated_fst_values):
    """
    Calculate the p-value for an observed Fst given a distribution of simulated Fst values.

    Parameters:
    observed_fst (float): The observed Fst value.
    simulated_fst_values (list or np.array): A list or array of simulated Fst values.

    Returns:
    float: The p-value.
    """
    simulated_fst_values = np.array(simulated_fst_values)

    # Number of simulated Fst values greater than or equal to the observed Fst
    num_extreme_values = np.sum(simulated_fst_values >= observed_fst)

    # Total number of simulations
    num_simulations = len(simulated_fst_values)

    # Calculate the p-value
    # Adding a small constant (1) to the numerator and denominator to avoid p-value of exactly 0
    p_value = (num_extreme_values + 1) / (num_simulations + 1)

    return p_value

def match_file_name(file_name, directory):
    """
    Match file names in the specified directory based on the given file name pattern.

    Parameters:
    file_name (str): The file name pattern to match.
    directory (str): The directory to search for matching files.

    Returns:
    str: The matched file path or None if no match is found.
    """
    base_name = file_name.replace('.csv', '')
    country1, country2 = base_name.split('_vs_')
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('_Simulated_Fst.csv'):
                if (country1 in file and country2 in file) or (country2 in file and country1 in file):
                    return os.path.join(root, file)
    return None

def main(input_file, directory, output_file):
    # Read the input file
    observed_df = pd.read_csv(input_file)

    # Prepare the output DataFrame
    results = []

    for index, row in observed_df.iterrows():
        file_name = row['File Name']
        observed_fst = row['Average FST']

        # Match the file name in the specified directory
        matched_file_path = match_file_name(file_name, directory)

        if matched_file_path:
            # Read the matched simulated Fst file
            simulated_df = pd.read_csv(matched_file_path)
            simulated_fst_values = simulated_df['simulated_Fst_averages']

            # Calculate the p-value
            p_value = calculate_p_value(observed_fst, simulated_fst_values)

            # Append the result
            results.append([file_name, observed_fst, p_value])
        else:
            print(f"Warning: No match found for {file_name}")

    # Create a DataFrame for the results
    results_df = pd.DataFrame(results, columns=['File Name', 'Observed_Fst_Average', 'P-value'])

    # Save the results to the output file
    results_df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate p-values for observed Fst values.")
    parser.add_argument("-i", "--input", required=True, help="Input CSV file containing observed Fst values.")
    parser.add_argument("-d", "--directory", required=True, help="Directory containing simulated Fst CSV files.")
    parser.add_argument("-o", "--output", required=True, help="Output CSV file to save the results.")

    args = parser.parse_args()

    main(args.input, args.directory, args.output)

