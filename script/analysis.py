import os
import json
import pandas as pd
from scipy import stats
from utils import calculate_statistics

# Folder to store the analysis results
analyses_folder = "analyses"

os.makedirs(analyses_folder, exist_ok=True)

def z_test_proportion(observed_proportion, expected_proportion, n):
    std_error = (expected_proportion * (1 - expected_proportion) / n) ** 0.5
    z_stat = (observed_proportion - expected_proportion) / std_error
    p_value = 1 - stats.norm.cdf(z_stat)
    return z_stat, p_value

def hypothesis_1(statistics):
    total_participants = statistics.get("total_participants", 0)
    female_participants = statistics.get("female_participants", 0)
    expected_female_proportion = 0.4652  # proportion of females in schools

    # Calculate observed female participation proportion
    observed_female_proportion = female_participants / total_participants if total_participants > 0 else 0

    # Perform Z-test for proportions
    z_stat, p_value = z_test_proportion(observed_female_proportion, expected_female_proportion, total_participants)

    # Prepare the result dictionary
    result = {
        "id": 1,
        "description": "Girls participate more in extracurricular activities (Olympiads) than boys in 2025",
        "z_statistic": z_stat,
        "p_value": p_value,
        "observed_female_proportion": observed_female_proportion,
        "expected_female_proportion": expected_female_proportion,
        "conclusion": "Reject the null hypothesis" if p_value < 0.05 else "Fail to reject the null hypothesis"
    }

    # Save results to JSON file for Hypothesis 1
    with open(os.path.join(analyses_folder, "hypothesis1.json"), "w") as f:
        json.dump(result, f, indent=4)

    return result

# Load statistics (you can modify this to get data from CSV or database if needed)
def load_statistics():
    data_csv_base = "/home/student/Desktop/Statistics Project/data/data_csv"
    statistics = calculate_statistics(data_csv_base)  # Calling the utility function to calculate statistics
    return statistics

# Main method to run the analysis
def perform_analysis():
    # Load or calculate the statistics
    statistics = load_statistics()

    # Hypothesis 1 Testing
    hypothesis_1_result = hypothesis_1(statistics)
    print("Hypothesis 1 Test Result:", hypothesis_1_result)

if __name__ == "__main__":
    perform_analysis()
