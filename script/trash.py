import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Data: Seeds (X) and Yield (Y)
seeds = np.array([4.2, 4.4, 4.6, 4.8, 5.0, 5.2, 5.4, 5.6, 5.8, 6.0])
yield_data = np.array([51, 54, 69, 81, 75, 79, 89, 101, 98, 102])

# Sample means
X_bar = np.mean(seeds)
Y_bar = np.mean(yield_data)
print(f"Mean of seeds: {X_bar}")
print(f"Mean of yield: {Y_bar}")

# Sample covariance (S_XY) and sample variance of X (S_XX)
S_XY = np.sum((seeds - X_bar) * (yield_data - Y_bar))
S_XX = np.sum((seeds - X_bar) ** 2)
print(f"S_XY: {S_XY}")
print(f"S_XX: {S_XX}")

# Compute linear regression parameters: slope (beta_1) and intercept (beta_0)
beta_1 = S_XY / S_XX  # Slope
beta_0 = Y_bar - beta_1 * X_bar  # Intercept
print(f"Regression equation: Yield = {beta_0:.2f} + {beta_1:.2f} × Seeds")

# Calculate fitted values and residuals
y_hat = beta_0 + beta_1 * seeds
residuals = yield_data - y_hat

# Calculate Sum of Squares
SS_Total = np.sum((yield_data - Y_bar) ** 2)
SS_Regression = np.sum((y_hat - Y_bar) ** 2)
SS_Error = np.sum(residuals ** 2)

# Calculate R-squared
r_squared = SS_Regression / SS_Total
print(f"R-squared: {r_squared:.4f}")

# Calculate standard error of the slope
n = len(seeds)
SE_beta1 = np.sqrt(SS_Error / (n - 2)) / np.sqrt(S_XX)
print(f"Standard error of slope: {SE_beta1:.4f}")

# Calculate t-statistic and p-value for testing H0: beta_1 = 0
t_statistic = beta_1 / SE_beta1
df = n - 2
p_value = 2 * (1 - stats.t.cdf(abs(t_statistic), df))
print(f"t-statistic: {t_statistic:.4f}")
print(f"p-value: {p_value:.8f}")

# Predicted change in yield for 0.3 gram increase in seeds
change_in_yield = 0.3 * beta_1
print(f"Predicted change in yield for 0.3 gram increase: {change_in_yield:.2f} kg")

# Create a scatter plot with regression line
plt.figure(figsize=(10, 6))
plt.scatter(seeds, yield_data, color='blue', label='Data points')
x_line = np.linspace(min(seeds), max(seeds), 100)
y_line = beta_0 + beta_1 * x_line
plt.plot(x_line, y_line, color='red', label=f'Regression line: y = {beta_0:.2f} + {beta_1:.2f}x')
plt.xlabel('Seeds (grams)')
plt.ylabel('Yield (kg)')
plt.title('Linear Regression: Yield vs Seeds')
plt.grid(True)
plt.legend()
# To display the plot, you would use plt.show() in a normal environment