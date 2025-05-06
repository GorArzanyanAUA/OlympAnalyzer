import json
import pandas as pd
import matplotlib.pyplot as plt

# Read the JSON data from file
with open('/home/student/Desktop/Statistics Project/analyses/second_statistics.json', 'r') as file:
    data = json.load(file)

# List of regions to analyze
regions = [
    "Yerevan", "Ararat", "Aragatsotn", "Gegharkunik", "Kotayk", 
    "Lori", "Shirak", "Syunik", "Vayots Dzor", "Tavush", "Armavir"
]

# List of subjects
subjects = ["armenian25", "chemistry25", "history25", "english25", "physics25", "math25"]

# Create a dictionary to store regional data
regional_data = {}

# Extract total participants per region
for region in regions:
    region_key = f"total_{region}_participants"
    if region_key in data:
        regional_data[region] = {
            "total": data[region_key],
            "girls": data[f"girl_{region}_participants"],
            "boys": data[f"boy_{region}_participants"],
            "stem": 0,
            "non_stem": 0,
            "subjects": {}
        }
        
        # Extract subject-specific data for each region
        for subject in subjects:
            girl_key = f"{subject}_{region}_girl"
            boy_key = f"{subject}_{region}_boy"
            
            if girl_key in data and boy_key in data:
                regional_data[region]["subjects"][subject] = {
                    "girls": data[girl_key],
                    "boys": data[boy_key],
                    "total": data[girl_key] + data[boy_key]
                }
                if subject in ["math25", "physics25", "chemistry25"]:
                    regional_data[region]["stem"] += regional_data[region]["subjects"][subject]["total"]
                else:
                    regional_data[region]["non_stem"] += regional_data[region]["subjects"][subject]["total"]


# Print regional statistics
print("Regional Analysis of Participants")
print("=" * 50)

for region, stats in regional_data.items():
    print(f"\n{region} Region:")
    print(f"  Total participants: {stats['total']}")
    print(f"  Girls: {stats['girls']} ({stats['girls']/stats['total']*100:.1f}%)")
    print(f"  Boys: {stats['boys']} ({stats['boys']/stats['total']*100:.1f}%)")
    
    print("\n  Subject Distribution:")
    for subject, subject_stats in stats["subjects"].items():
        subject_name = subject.replace("25", "")
        print(f"    {subject_name.capitalize()}: {subject_stats['total']} participants " +
              f"({subject_stats['total']/stats['total']*100:.1f}% of region)")

# Create a pandas DataFrame for easier analysis and visualization
region_df = pd.DataFrame({
    'Region': list(regional_data.keys()),
    'Total': [stats['total'] for stats in regional_data.values()],
    'Girls': [stats['girls'] for stats in regional_data.values()],
    'Boys': [stats['boys'] for stats in regional_data.values()],
    'STEM': [stats['stem'] for stats in regional_data.values()],
    'Non_STEM': [stats['non_stem'] for stats in regional_data.values()]
})

# Sort by total participants
region_df = region_df.sort_values('Total', ascending=False)

# Calculate the percentage for visualization
region_df['Girls_Pct'] = region_df['Girls'] / region_df['Total'] * 100
region_df['Boys_Pct'] = region_df['Boys'] / region_df['Total'] * 100

print("\n\nRegional Comparison Summary:")
print(region_df[['Region', 'Total', 'Girls', 'Boys', 'STEM', 'Non_STEM']])

# Calculate subject participation across regions
subject_distribution = {subject: 0 for subject in subjects}
for region_stats in regional_data.values():
    for subject, subject_stats in region_stats["subjects"].items():
        subject_distribution[subject] += subject_stats['total']

# Print overall subject distribution
print("\nOverall Subject Distribution:")
for subject, count in subject_distribution.items():
    subject_name = subject.replace("25", "")
    percentage = count / data["total_participants"] * 100
    print(f"  {subject_name.capitalize()}: {count} participants ({percentage:.1f}%)")

# Optional: Create visualizations of the data
def plot_regional_distribution():
    plt.figure(figsize=(14, 8))
    
    # Create a horizontal bar chart
    plt.barh(region_df['Region'], region_df['Total'])
    plt.xlabel('Number of Participants')
    plt.ylabel('Region')
    plt.title('Total Participants by Region')
    
    # Add labels to the bars
    for index, value in enumerate(region_df['Total']):
        plt.text(value + 100, index, str(value))
    
    plt.tight_layout()
    plt.savefig('regional_distribution.png')
    plt.close()

def plot_gender_distribution():
    plt.figure(figsize=(14, 8))
    
    # Create a stacked bar chart
    plt.barh(region_df['Region'], region_df['Girls'], label='Girls')
    plt.barh(region_df['Region'], region_df['Boys'], left=region_df['Girls'], label='Boys')
    
    plt.xlabel('Number of Participants')
    plt.ylabel('Region')
    plt.title('Gender Distribution by Region')
    plt.legend()
    
    # Add percentage labels
    for index, region in enumerate(region_df['Region']):
        girl_count = region_df.loc[region_df['Region'] == region, 'Girls'].values[0]
        boy_count = region_df.loc[region_df['Region'] == region, 'Boys'].values[0]
        total = girl_count + boy_count
        girl_pct = girl_count / total * 100
        
        # Add girl percentage at the middle of the girl section
        plt.text(girl_count / 2, index, f"{girl_pct:.1f}%", va='center', ha='center')
        
        # Add boy percentage at the middle of the boy section
        plt.text(girl_count + boy_count / 2, index, f"{100-girl_pct:.1f}%", va='center', ha='center')
    
    plt.tight_layout()
    plt.savefig('gender_distribution.png')
    plt.close()

def plot_subject_distribution():
    # Create a new DataFrame for subject distribution
    subject_data = []
    for subject in subjects:
        subject_name = subject.replace("25", "")
        subject_data.append({
            'Subject': subject_name.capitalize(),
            'Count': subject_distribution[subject],
            'Percentage': subject_distribution[subject] / data["total_participants"] * 100
        })
    
    subject_df = pd.DataFrame(subject_data)
    subject_df = subject_df.sort_values('Count', ascending=False)
    
    plt.figure(figsize=(12, 6))
    plt.bar(subject_df['Subject'], subject_df['Count'])
    plt.xlabel('Subject')
    plt.ylabel('Number of Participants')
    plt.title('Subject Participation Distribution')
    
    # Add labels to the bars
    for index, value in enumerate(subject_df['Count']):
        percentage = subject_df.iloc[index]['Percentage']
        plt.text(index, value + 100, f"{value}\n({percentage:.1f}%)", ha='center')
    
    plt.tight_layout()
    plt.savefig('subject_distribution.png')
    plt.close()

# Uncomment the following lines to generate visualizations
# plot_regional_distribution()
# plot_gender_distribution()
# plot_subject_distribution()

print("\nAnalysis complete!")