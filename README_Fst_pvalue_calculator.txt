This is a README for Fst_pvalue_calculator.py 

This script has three user options 

-i = Observed_Fst_values.csv 

File format
 
File Name,Average FST
Indonesia_vs_Myanmar,0.08791937037999997

-d = directory containing Estimated Fst files 
File name structure: Cambodia_vs_Cameroon_Simulated_Fst.csv

File Format 

simulated_run,simulated_Fst_averages
Myanmar_vs_Indonesia_sim_1,0.003032582872

-o = output.csv containing all assessed Fst p-values 

Version Notes:
Version 2 - corrected incorrect identification of -d .csv file columns
Version 3 - added 1 to numerator/denominator of p-value calculcations to prevent p-values = 0 

Explanation:
Adjusting p-value Calculation:
To avoid a p-value of exactly 0, we add 1 to both the numerator and the denominator in the p-value calculation: 
p_value = (num_extreme_values + 1) / (num_simulations + 1).
This adjustment ensures that even if no simulated values are greater than or equal to the observed value, the p-value will be slightly above 0.
This adjustment helps make the p-value calculation more robust and avoids the issue of having p-values exactly equal to 0, 
which can be problematic in some statistical analyses.

-----------------------------------------------------------------------

Script process

Step 1) identify File Name from observed Fst file row 1

Step 2) parse through -d directory for any file that has Country1_vs_Country2 or Country_vs_Country1 that match File Name from -i .csv 

Step 3) Extract average Fst from corresponding second column in observed Fst.csv and places it on the distribution of simulated Fst's from the corresponding
file in -d directory 

Step 4) prints File Name, Observed Fst and P-value to an output file specified by -o 

------------------------------------------------------------------------

How p-values are calculated:

############
Basic script:

import numpy as np

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
    p_value = num_extreme_values / num_simulations
    
    return p_value

# Example usage
observed_fst = 0.15  # Replace with your observed Fst value
simulated_fst_values = np.random.normal(0.1, 0.02, 1000)  # Replace with your simulated Fst values

p_value = calculate_p_value(observed_fst, simulated_fst_values)
print(f"P-value: {p_value}")

##########
Explanation
Input Parameters:

observed_fst: The observed Fst value that you want to test.
simulated_fst_values: A list or array of simulated Fst values generated from bootstrapping.
Convert the simulated Fst values to a numpy array: This allows for efficient computation using numpy operations.

Count the number of simulated Fst values greater than or equal to the observed Fst: This is done using np.sum(simulated_fst_values >= observed_fst).

Calculate the p-value: The p-value is the proportion of simulated Fst values that are as extreme or more extreme than the observed Fst value, 
calculated as num_extreme_values / num_simulations.

Considerations
One-tailed vs Two-tailed Tests: The script above assumes a one-tailed test (testing if the observed Fst is greater than or equal to the simulated Fst 
values). If a two-tailed test is required, you will need to adjust the calculation to account for values both greater than and less than the observed Fst.

Edge Cases: If the observed Fst is outside the range of the simulated values (e.g., all simulated values are less than the observed Fst), 
the p-value will be very small, indicating a significant result.

Random Seed: Ensure that the simulated values are reproducible if needed by setting a random seed before generating them (e.g., np.random.seed(42)).

This script provides a straightforward way to calculate the p-value for an observed Fst value based on a distribution of simulated Fst values. 
Adjust the script as needed based on your specific requirements and the direction of your hypothesis test.
