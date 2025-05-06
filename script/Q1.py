import pandas as pd
import numpy as np
from scipy.stats import chisquare
import matplotlib.pyplot as plt
import seaborn as sns

# Given regional population counts (school enrollment)
region_population = {
    "Yerevan": 144166,
    "Aragatsotn": 19357,
    "Ararat": 42084,
    "Gegharkunik": 28998,
    "Kotayk": 43658,
    "Lori": 31907,
    "Shirak": 32448,
    "Syunik": 17934,
    "Vayots Dzor": 6998,
    "Tavush": 17384,
    "Armavir": 40013
}

# Given observed olympiad participation by region
observed_participation = {
    "Yerevan": 16316,
    "Aragatsotn": 3039,
    "Ararat": 4868,
    "Gegharkunik": 4863,
    "Kotayk": 7074,
    "Lori": 5522,
    "Shirak": 5155,
    "Syunik": 4015,
    "Vayots Dzor": 1517,
    "Tavush": 3020,
    "Armavir": 4562
}

# Total population across regions and total olympiad participants
total_population = sum(region_population.values())
total_olympiad = sum(observed_participation.values())

# Calculate the overall participation rate
overall_rate = total_olympiad / total_population

# Compute actual and expected participation rates
results = []
for region in region_population:
    pop = region_population[region]
    obs = observed_participation[region]
    
    # Actual participation rate for the region
    actual_rate = obs / pop
    
    # Expected participation would simply be the overall rate
    expected_rate = overall_rate
    
    # Calculate expected participation count based on population
    expected_count = pop * overall_rate
    
    results.append({
        "Region": region,
        "Population": pop,
        "Observed": obs,
        "Expected Count": expected_count,
        "Actual Rate": actual_rate * 100,  # Convert to percentage
        "Expected Rate": expected_rate * 100,  # Convert to percentage
        "Rate Difference": (actual_rate - expected_rate) * 100  # Difference in percentage points
    })

# Create DataFrame
df = pd.DataFrame(results)

# Perform chi-square goodness-of-fit test
observed = df["Observed"].values
expected = df["Expected Count"].values
chi2_stat, p_value = chisquare(f_obs=observed, f_exp=expected)

# Sort by Rate Difference for better visualization
df_sorted = df.sort_values("Rate Difference", ascending=False)

# Create visualization comparing actual vs expected rates
plt.figure(figsize=(10, 5))

# Set the width of the bars
bar_width = 0.35

# Set up positions for the bars
indices = np.arange(len(df_sorted))

# Create the bars
plt.bar(indices - bar_width/2, df_sorted["Actual Rate"], 
        width=bar_width, color='darkblue', label='Actual Rate (%)')
plt.bar(indices + bar_width/2, df_sorted["Expected Rate"], 
        width=bar_width, color='lightblue', label='Expected Rate (%)')

# Add a horizontal line for the overall average rate
plt.axhline(y=overall_rate*100, color='red', linestyle='--', 
           label=f'National Average: {overall_rate*100:.2f}%')

# Customizing the plot
plt.xlabel('Region', fontsize=12)
plt.ylabel('Participation Rate (%)', fontsize=12)
plt.title('Comparison of Actual vs Expected Olympiad Participation Rates by Region', fontsize=14)
plt.xticks(indices, df_sorted["Region"], rotation=45, ha='right')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add value labels on top of bars
for i, v in enumerate(df_sorted["Actual Rate"]):
    plt.text(i - bar_width/2, v + 0.3, f'{v:.1f}%', 
             ha='center', va='bottom', fontsize=9, rotation=0)

for i, v in enumerate(df_sorted["Expected Rate"]):
    plt.text(i + bar_width/2, v + 0.3, f'{v:.1f}%', 
             ha='center', va='bottom', fontsize=9, rotation=0)

# Add rate difference as text between bars
for i, row in enumerate(df_sorted.itertuples()):
    diff = row._6  # Index position of "Rate Difference" column
    actual = row._4  # Index position of "Actual Rate" column
    expected = row._5  # Index position of "Expected Rate" column
    color = 'green' if diff > 0 else 'red'
    plt.text(i, max(actual, expected) + 1.5, 
             f'{diff:+.1f}%', 
             ha='center', va='bottom', fontsize=10, fontweight='bold', color=color)

plt.tight_layout()

# Display chi-square results
print(f"Chi-square statistic: {chi2_stat:.2f}")
print(f"P-value: {p_value:.10e}")
print("\nComparison of Regional Participation Rates:")
print(df_sorted[["Region", "Actual Rate", "Expected Rate", "Rate Difference"]].round(2).to_string(index=False))

# Create a second chart showing the absolute numbers
plt.figure(figsize=(8, 5))

# Create the bars for absolute numbers
plt.bar(indices - bar_width/2, df_sorted["Observed"], 
        width=bar_width, color='darkgreen', label='Observed Participants')
plt.bar(indices + bar_width/2, df_sorted["Expected Count"], 
        width=bar_width, color='lightgreen', label='Expected Participants')

# Customizing the second plot
plt.xlabel('Region', fontsize=12)
plt.ylabel('Number of Participants', fontsize=12)
plt.title('Comparison of Observed vs Expected Olympiad Participants by Region', fontsize=14)
plt.xticks(indices, df_sorted["Region"], rotation=45, ha='right')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add value labels on top of bars for absolute numbers
for i, v in enumerate(df_sorted["Observed"]):
    plt.text(i - bar_width/2, v + 100, f'{int(v)}', 
             ha='center', va='bottom', fontsize=9, rotation=0)

for i, v in enumerate(df_sorted["Expected Count"]):
    plt.text(i + bar_width/2, v + 100, f'{int(v)}', 
             ha='center', va='bottom', fontsize=9, rotation=0)

plt.tight_layout()

# Show the plots
plt.show()