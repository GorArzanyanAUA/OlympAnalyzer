import json
import os
import pandas as pd


def calculate_statistics(data_csv_base):
    # Initialize statistics dictionary
    statistics = {
        "total_participants": 0,
        
        "yerevan_participants": 0,
        "region_participants": 0,
        
        "girl_participants": 0,
        "boy_participants": 0,
        
        "girl_yerevan_participants": 0,
        "girl_region_participants": 0,
        
        "boy_yerevan_participants": 0,
        "boy_region_participants": 0
    }

    # Walk through CSV files and process data
    for root, dirs, files in os.walk(data_csv_base):
        for file in files:
            if file.endswith(".csv"):
                filepath = os.path.join(root, file)
                print(f"\n📄 Processing: {file}")
                try:
                    df = pd.read_csv(filepath)
                    
                    # Ensure 'gender' and 'region' columns are present
                    if 'gender' in df.columns and 'region' in df.columns:
                        # Iterate through each row and update statistics
                        for _, row in df.iterrows():
                            gender = row['gender'].lower()
                            region = row['region']

                            # Total participants
                            statistics["total_participants"] += 1

                            # Yerevan participants
                            if region == "Երևան":
                                statistics["yerevan_participants"] += 1

                            # Regional participants
                            if region != "Երևան":
                                statistics["region_participants"] += 1

                            # girl participants
                            if gender == "girl":
                                statistics["girl_participants"] += 1
                                if region == "Երևան":
                                    statistics["girl_yerevan_participants"] += 1

                                if region != "Երևան":
                                    statistics["girl_region_participants"] += 1

                            # boy participants
                            if gender == "boy":
                                statistics["boy_participants"] += 1
                                if region == "Երևան":
                                    statistics["boy_yerevan_participants"] += 1
                                if region != "Երևան":
                                    statistics["boy_region_participants"] += 1
                    else:
                        print(f"Skipped: Missing 'gender' or 'region' column in {file}")
                except Exception as e:
                    print(f"Error processing {file}: {e}")

    # Save the calculated statistics to a new JSON file
    output_file = "calculated_statistics.json"
    with open(output_file, "w") as f:
        json.dump(statistics, f, indent=4)

    print(f"✅ Statistics calculated and saved to {output_file}")
    return statistics


def read_data_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        # If the file does not exist, return an empty dictionary
        return {}
    except json.JSONDecodeError:
        print("Error decoding JSON. Please check the file.")
        return {}

def save_data_to_file(file_path, data):
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
            print(f"✅ Data saved to {file_path}")
    except Exception as e:
        print(f"❌ Failed to save data: {e}")

def add_or_update_statistic(data, subject, year, metric_name, value):
    # Check if subject and year exist, if not create them
    if subject not in data:
        data[subject] = {}
    if year not in data[subject]:
        data[subject][year] = {}

    # Update or add the new statistic
    data[subject][year][metric_name] = value

    # Save the updated data to the file
    save_data_to_file('statistics.json', data)


