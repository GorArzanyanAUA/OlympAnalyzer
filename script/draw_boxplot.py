import matplotlib.pyplot as plt
import numpy as np
import json

# Load the statistics from the JSON file
def load_statistics(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# Example data for boxplot: Number of participants for Girls and Boys in different regions
regions = ['Yerevan', 'Ararat', 'Aragatsotn', 'Gegharkunik', 'Kotayk', 'Lori', 'Shirak', 'Syunik', 'Vayots Dzor', 'Tavush', 'Armavir']
subjects = ['math25', 'physics25', 'chemistry25', 'armenian25', 'english25', 'history25']
file_path = '/home/student/Desktop/Statistics Project/analyses/calculated_statistics_with_subject_region_gender.json'  # Update this path

statistics = load_statistics(file_path)
girls_participation = [[] for _ in range(len(regions))]
boys_participation = [[] for _ in range(len(regions))]
for id, region in enumerate(regions):
    for subject in subjects:
        # print(f"Processing {subject} for {region}")
        # print(statistics.get(f'{subject}_{region}_girl'))
        # print(statistics.get(f'{subject}_{region}_boy'))
        girls_participation[id].append(statistics.get(f'{subject}_{region}_girl'))
        boys_participation[id].append(statistics.get(f'{subject}_{region}_boy'))


# for i in range(len(regions)):
#     print(f"Region: {regions[i]}")
#     print(girls_participation[i])
# Create figure and axis
fig, ax = plt.subplots(figsize=(7, 6))

# # Create positions for the boxplots
positions = np.arange(1, len(regions) * 3, 3)  # More space between region groups

# Create boxplots with different colors for girls and boys
girls_boxes = ax.boxplot([girls_participation[i] for i in range(len(regions))], 
                        positions=positions, 
                        widths=0.6, 
                        patch_artist=True,
                        medianprops=dict(color='black', linewidth=1.5),
                        boxprops=dict(facecolor='#8ABDE6', color='black'),  # Light blue for girls
                        whiskerprops=dict(color='black', linewidth=1),
                        capprops=dict(color='black', linewidth=1),
                        flierprops=dict(marker='o', markerfacecolor='#8ABDE6', markersize=5))

boys_boxes = ax.boxplot([boys_participation[i] for i in range(len(regions))], 
                       positions=positions + 1,  # Offset to place next to girls
                       widths=0.6, 
                       patch_artist=True,
                       medianprops=dict(color='black', linewidth=1.5),
                       boxprops=dict(facecolor='#90EE90', color='black'),  # Light green for boys
                       whiskerprops=dict(color='black', linewidth=1),
                       capprops=dict(color='black', linewidth=1),
                       flierprops=dict(marker='o', markerfacecolor='#90EE90', markersize=5))

# Set labels
ax.set_xticks(positions + 0.5)  # Position labels between the pairs of boxplots
ax.set_xticklabels(regions, rotation=45, ha="center", fontsize=11)
ax.set_ylabel('Number of Participants', fontsize=11, fontweight='bold')
ax.set_xlabel('Region', fontsize=11, fontweight='bold')

# Add a grid for better readability
ax.yaxis.grid(True, linestyle='--', alpha=0.7)

# Set y-axis limits
ax.set_ylim(-10, 4500)

# Add legend
girls_patch = plt.Rectangle((0, 0), 1, 1, fill=True, facecolor='#8ABDE6', edgecolor='black')
boys_patch = plt.Rectangle((0, 0), 1, 1, fill=True, facecolor='#90EE90', edgecolor='black')
ax.legend([girls_patch, boys_patch], ['Girls', 'Boys'], loc='upper right')

# Title
# Show plot
plt.tight_layout()
plt.show()

# Save the figure
plt.savefig('region_gender_boxplot.png', dpi=300, bbox_inches='tight')
    