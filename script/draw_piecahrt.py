import matplotlib.pyplot as plt

def plot_pie_chart(stem_participants, non_stem_participants, save_path='stem_non_stem_pie_chart.png'):
    # Data for pie chart
    labels = ['STEM', 'Non-STEM']
    sizes = [stem_participants, non_stem_participants]
    colors = ['#66b3ff', '#ffb3e6']
    explode = (0.1, 0)  # explode the first slice (STEM) slightly

    # Create a pie chart
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)

    # Equal aspect ratio ensures that pie chart is drawn as a circle.
    ax.axis('equal')

    # Title
    plt.title('Proportion of STEM vs Non-STEM Participants, Yerevan', fontsize=10)

    # Save the chart
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')

    # Show the chart
    plt.show()

# Total 
non_stem_participants = 21889  
stem_participants = 38022  


# # Yerevan
# non_stem_participants = 4705  
# stem_participants = 11605  


# # Region
# non_stem_participants = 17288  
# stem_participants = 26522  

# Call the function to plot the pie chart
plot_pie_chart(stem_participants, non_stem_participants)
