import matplotlib.pyplot as plt
import numpy as np
import json

# Load the statistics from the JSON file
def load_statistics(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# import matplotlib.pyplot as plt
# import numpy as np
# # Data from tables: Number of participants by region and gender
# List of regions
# regions = ['Yerevan', 'Ararat', 'Aragatsotn', 'Gegharkunik', 'Kotayk', 'Lori', 'Shirak', 'Syunik', 'Vayots Dzor', 'Tavush', 'Armavir']

# # Girls' participation data
# girls_participation = [8358, 3063, 1913, 3126, 4527, 3420, 3159, 2390, 973, 1889, 2908]

# # Boys' participation data
# boys_participation = [7952, 1800, 1125, 1736, 2546, 2096, 1990, 1624, 544, 1125, 1647]

# # Plotting the bar chart
# fig, ax = plt.subplots(figsize=(8, 5))

# # Set width for the bars
# bar_width = 0.35

# # Set positions for bars on the X-axis
# index = np.arange(len(regions))

# # Plotting bars for girls and boys
# bar1 = ax.bar(index, girls_participation, bar_width, label='Girls', color='#4472C4')
# bar2 = ax.bar(index + bar_width, boys_participation, bar_width, label='Boys', color='#70AD47')

# # Adding labels, title, and customizing the axes
# ax.set_xlabel('Region')
# ax.set_ylabel('Number of Participants')
# ax.set_title('Number of Students Participating by Region and Gender')
# ax.set_xticks(index + bar_width / 2)
# ax.set_xticklabels(regions, rotation=45, ha='right')
# ax.legend()

# # Display the chart
# plt.tight_layout()
# plt.show()

# # Function to plot STEM subjects participation
def plot_stem_participation(regions, stem_girls_total, stem_boys_total):
    bar_width = 0.35
    index = np.arange(len(regions))
    
    fig, ax = plt.subplots(figsize=(5, 3))
    bar1 = ax.bar(index, stem_girls_total, bar_width, label='Girls (STEM)', color='lightblue')
    bar2 = ax.bar(index + bar_width, stem_boys_total, bar_width, label='Boys (STEM)', color='lightgreen')

    # Adding labels, title, and customizing the axes for STEM subjects
    ax.set_xlabel('Region')
    ax.set_ylabel('Number of Participants')
    ax.set_title('STEM Subject Participation by Region and Gender')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(regions, rotation=45, ha='right')
    ax.legend()

    # Show the STEM chart
    plt.tight_layout()
    plt.show()

# Function to plot Non-STEM subjects participation
def plot_non_stem_participation(regions, non_stem_girls_total, non_stem_boys_total):
    bar_width = 0.35
    index = np.arange(len(regions))
    
    fig, ax = plt.subplots(figsize=(5, 3))
    bar1 = ax.bar(index, non_stem_girls_total, bar_width, label='Girls (Non-STEM)', color='coral')
    bar2 = ax.bar(index + bar_width, non_stem_boys_total, bar_width, label='Boys (Non-STEM)', color='yellow')

    # Adding labels, title, and customizing the axes for Non-STEM subjects
    ax.set_xlabel('Region')
    ax.set_ylabel('Number of Participants')
    ax.set_title('Non-STEM Subject Participation by Region and Gender')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(regions, rotation=45, ha='right')
    ax.legend()

    # Show the Non-STEM chart
    plt.tight_layout()
    plt.show()

# Main function to load data and plot the charts
def main():
    # File path to the JSON file with statistics
    file_path = '/home/student/Desktop/Statistics Project/analyses/calculated_statistics_with_subject_region_gender.json'  # Update this path
    statistics = load_statistics(file_path)

    # Extract regions and corresponding participation data for STEM and Non-STEM subjects
    regions = ['Yerevan', 'Ararat', 'Aragatsotn', 'Gegharkunik', 'Kotayk', 'Lori', 'Shirak', 'Syunik', 'Vayots Dzor', 'Tavush', 'Armavir']

    # STEM subjects
    stem_subjects = ['math25', 'physics25', 'chemistry25']
    stem_girls_total = []
    stem_boys_total = []

    for region in regions:
        total_girls_stem = sum([statistics.get(f'{subject}_{region}_girl', {}) for subject in stem_subjects])
        total_boys_stem = sum([statistics.get(f'{subject}_{region}_boy', {}) for subject in stem_subjects])
        stem_girls_total.append(total_girls_stem)
        stem_boys_total.append(total_boys_stem)

    # Non-STEM subjects
    non_stem_subjects = ['armenian25', 'english25', 'history25']
    non_stem_girls_total = []
    non_stem_boys_total = []

    for region in regions:
        total_girls_non_stem = sum([statistics.get(f'{subject}_{region}_girl', {}) for subject in non_stem_subjects])
        total_boys_non_stem = sum([statistics.get(f'{subject}_{region}_boy', {}) for subject in non_stem_subjects])
        non_stem_girls_total.append(total_girls_non_stem)
        non_stem_boys_total.append(total_boys_non_stem)

    # Plot STEM and Non-STEM participation
    plot_stem_participation(regions, stem_girls_total, stem_boys_total)
    plot_non_stem_participation(regions, non_stem_girls_total, non_stem_boys_total)

# Call the main function to execute the plotting
if __name__ == "__main__":
    main()
