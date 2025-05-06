import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

# Define the number of participants for each region and each subject (STEM and non-STEM)
regions = [
    'Yerevan', 'Ararat', 'Aragatsotn', 'Gegharkunik', 'Kotayk', 'Lori', 'Shirak', 'Syunik', 'Vayots Dzor', 'Tavush', 'Armavir'
]

# Define the number of participants for each subject in each region
data = {
    'Region': regions,
    'Math_Girls': [4337, 1305, 823, 1092, 1718, 1605, 1289, 1090, 354, 738, 1143],
    'Math_Boys': [5804, 1293, 764, 999, 1674, 1434, 1296, 1127, 333, 749, 1037],
    'Physics_Girls': [333, 167, 83, 312, 154, 160, 171, 79, 49, 81, 139],
    'Physics_Boys': [653, 135, 59, 250, 117, 111, 141, 97, 32, 72, 98],
    'Chemistry_Girls': [289, 210, 97, 196, 216, 135, 192, 107, 68, 105, 158],
    'Chemistry_Boys': [189, 72, 40, 55, 80, 68, 80, 52, 21, 44, 51],
    'Armenian_Girls': [1370, 813, 449, 727, 883, 693, 750, 529, 237, 517, 553],
    'Armenian_Boys': [304, 143, 93, 155, 172, 141, 190, 124, 63, 105, 114],
    'History_Girls': [598, 0, 236, 481, 405, 371, 405, 202, 137, 233, 555],
    'History_Boys': [339, 0, 97, 181, 165, 170, 137, 95, 54, 98, 229],
    'English_Girls': [1431, 568, 225, 318, 1151, 456, 352, 383, 128, 215, 360],
    'English_Boys': [663, 157, 72, 96, 338, 172, 146, 129, 41, 57, 118]
}

# Create DataFrame from the above data
df = pd.DataFrame(data)

# Calculate the total for STEM (Math + Physics + Chemistry)
df['STEM_Girls'] = df['Math_Girls'] + df['Physics_Girls'] + df['Chemistry_Girls']
df['STEM_Boys'] = df['Math_Boys'] + df['Physics_Boys'] + df['Chemistry_Boys']

# Calculate the total for Non-STEM (Armenian + History + English)
df['Non_STEM_Girls'] = df['Armenian_Girls'] + df['History_Girls'] + df['English_Girls']
df['Non_STEM_Boys'] = df['Armenian_Boys'] + df['History_Boys'] + df['English_Boys']

# Sum the totals for each region
df['STEM_Total'] = df['STEM_Girls'] + df['STEM_Boys']
df['Non_STEM_Total'] = df['Non_STEM_Girls'] + df['Non_STEM_Boys']

# Calculate the grand total (N)
grand_total = df['STEM_Total'].sum() + df['Non_STEM_Total'].sum()

# Calculate the expected values (Eij)
total_stem = df['STEM_Total'].sum()
total_non_stem = df['Non_STEM_Total'].sum()

# Calculate the expected values for each region
df['Expected STEM'] = (df['STEM_Total'] * total_stem) / grand_total
df['Expected Non-STEM'] = (df['Non_STEM_Total'] * total_non_stem) / grand_total

# Perform the Chi-square test of independence
observed = np.array([df['STEM_Total'], df['Non_STEM_Total']]).T

# Perform chi-square test
chi2_stat, p_val, dof, expected = chi2_contingency(observed)

# Print the results
print(f"Chi-square Statistic: {chi2_stat}")
print(f"P-value: {p_val}")
print(f"Degrees of Freedom: {dof}")
print(f"Expected Counts Table:\n{expected}")

# Conclusion based on the p-value
if p_val < 0.05:
    print("We reject the null hypothesis, meaning there is a significant relationship between region and subject interest.")
else:
    print("We fail to reject the null hypothesis, meaning there is no significant relationship between region and subject interest.")
