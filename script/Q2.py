import math
from scipy.stats import norm

# Data - You need to replace these values with the actual numbers from your dataset
total_students = 59911  # Total number of students
students_in_stem = 38022  # Number of students interested in STEM subjects

# Null hypothesis value for p0
p0 = 0.5

# Proportion of students interested in STEM
p_hat = students_in_stem / total_students

# Z-test statistic
z = (p_hat - p0) / math.sqrt(p0 * (1 - p0) / total_students)

# Calculate the p-value (two-tailed test)
p_value = 2 * (1 - norm.cdf(abs(z)))

# Print the Z-statistic and p-value
print(f"Z-test statistic: {z:.4f}")
print(f"P-value: {p_value:.4f}")

# Significance level (alpha)
alpha = 0.05

# Decision rule: Reject H0 if p-value is less than alpha
if p_value < alpha:
    print("Reject the null hypothesis: There is a significant preference towards STEM or non-STEM subjects.")
else:
    print("Fail to reject the null hypothesis: There is no significant preference towards STEM or non-STEM subjects.")


p_hat = students_in_stem / total_students

# Confidence level for 95% CI (Z-value for 95% is 1.96)
z_value = 1.96

# Calculate the standard error (SE) for the proportion
se = math.sqrt(p_hat * (1 - p_hat) / total_students)

# Calculate the margin of error
margin_of_error = z_value * se

# Calculate the confidence interval
lower_bound = p_hat - margin_of_error
upper_bound = p_hat + margin_of_error

# Display the results
print(f"Sample Proportion (p̂): {p_hat:.4f}")
print(f"Standard Error (SE): {se:.4f}")
print(f"Margin of Error: {margin_of_error:.4f}")
print(f"95% Confidence Interval: ({lower_bound:.4f}, {upper_bound:.4f})")