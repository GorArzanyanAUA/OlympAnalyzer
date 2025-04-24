import json
import os
import pandas as pd

# Dictionary mapping Armenian region names to their Latin equivalents
armenia_regions_latins = {
    "Արարատ": "Ararat",
    "Արագածոտն": "Aragatsotn",
    "Գեղարքունիք": "Gegharkunik",
    "Կոտայք": "Kotayk",
    "Լոռի": "Lori",
    "Շիրակ": "Shirak",
    "Սյունիք": "Syunik",
    "Վայոց": "Vayots Dzor",
    "Տավուշ": "Tavush",
    "Արմավիր": "Armavir"
}

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
        "boy_region_participants": 0,
        "unclassified_participants": 0,  # Unclassified participants
    }

    # Initialize dictionary to track region-wise statistics using Latin names
    region_counts = {latin_name: {"total": 0, "girl": 0, "boy": 0} for latin_name in armenia_regions_latins.values()}

    # Initialize dictionary to track participants per subject
    subject_participants = {}

    # Walk through CSV files and process data
    for root, dirs, files in os.walk(data_csv_base):
        for file in files:
            if file.endswith(".csv"):
                filepath = os.path.join(root, file)

                # Extract subject name from the folder name (assuming folder name is the subject)
                subject = os.path.basename(root)  # Folder name is the subject (e.g., math25, physics25)
                print(f"📄 Processing {file} under subject {subject}")

                # Initialize subject statistics if not already
                if subject not in subject_participants:
                    subject_participants[subject] = 0

                try:
                    df = pd.read_csv(filepath)

                    # Ensure 'gender' and 'region' columns are present
                    if 'gender' in df.columns and 'region' in df.columns:
                        # Iterate through each row and update statistics
                        for _, row in df.iterrows():
                            gender = row['gender'].lower() if pd.notna(row['gender']) else None
                            region = row['region'] if pd.notna(row['region']) else None

                            # Total participants
                            statistics["total_participants"] += 1
                            subject_participants[subject] += 1  # Increment the subject participant count

                            # Yerevan participants
                            if region == "Երևան":
                                statistics["yerevan_participants"] += 1
                            elif region in armenia_regions_latins:
                                statistics["region_participants"] += 1
                                latin_region = armenia_regions_latins.get(region, region)  # Get the Latin name for the region
                                region_counts[latin_region]["total"] += 1
                            else:
                                statistics["unclassified_participants"] += 1  # Unclassified participants

                            # Classify by gender
                            if gender == "girl":
                                statistics["girl_participants"] += 1
                                if region == "Երևան":
                                    statistics["girl_yerevan_participants"] += 1
                                elif region in armenia_regions_latins:
                                    statistics["girl_region_participants"] += 1
                                    latin_region = armenia_regions_latins.get(region, region)  # Get the Latin name for the region
                                    region_counts[latin_region]["girl"] += 1
                            elif gender == "boy":
                                statistics["boy_participants"] += 1
                                if region == "Երևան":
                                    statistics["boy_yerevan_participants"] += 1
                                elif region in armenia_regions_latins:
                                    statistics["boy_region_participants"] += 1
                                    latin_region = armenia_regions_latins.get(region, region)  # Get the Latin name for the region
                                    region_counts[latin_region]["boy"] += 1
                            else:
                                statistics["unclassified_participants"] += 1  # Unclassified participants

                    else:
                        print(f"⚠️ Skipped: Missing 'gender' or 'region' column in {file}")

                except Exception as e:
                    print(f"❌ Error processing {file}: {e}")

                # Check if the Latin region name exists in the filename
                for latin_region in armenia_regions_latins.values():
                    if latin_region.lower() in file.lower():  # Case-insensitive check
                        print(f"⚡ Found region {latin_region} in filename. Updating statistics...")
                        # Increment statistics for the region in the file name
                        if latin_region in region_counts:
                            region_counts[latin_region]["total"] += 1
                            statistics["unclassified_participants"] -= 1  # Deduct from unclassified
                            break

    # Add region-wise statistics to the main statistics dictionary
    for region, counts in region_counts.items():
        statistics[f"total_{region}_participants"] = counts["total"]
        statistics[f"girl_{region}_participants"] = counts["girl"]
        statistics[f"boy_{region}_participants"] = counts["boy"]

    # Add subject statistics to the main statistics dictionary
    for subject, count in subject_participants.items():
        statistics[f"{subject}_participants"] = count

    # Save the calculated statistics to a new JSON file
    output_folder = "/home/student/Desktop/Statistics Project/analyses/"
    output_file = "calculated_statistics.json"
    with open(output_folder+output_file, "w") as f:
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


def check_data_consistency(statistics):
    # Check if total participants match the sum of boys and girls
    total_girls_and_boys = statistics["girl_participants"] + statistics["boy_participants"]
    if total_girls_and_boys != statistics["total_participants"]:
        print(f"❌ Total participants mismatch! {total_girls_and_boys} != {statistics['total_participants']}")
    else:
        print("✅ Total participants check passed.")
    
    # Check if Yerevan participants match the sum of girls and boys in Yerevan
    yerevan_girls_and_boys = statistics["girl_yerevan_participants"] + statistics["boy_yerevan_participants"]
    if yerevan_girls_and_boys != statistics["yerevan_participants"]:
        print(f"❌ Yerevan participants mismatch! {yerevan_girls_and_boys} != {statistics['yerevan_participants']}")
    else:
        print("✅ Yerevan participants check passed.")
    
    # Check if Region participants match the sum of girls and boys in regions
    region_girls_and_boys = statistics["girl_region_participants"] + statistics["boy_region_participants"]
    if region_girls_and_boys != statistics["region_participants"]:
        print(f"❌ Region participants mismatch! {region_girls_and_boys} != {statistics['region_participants']}")
    else:
        print("✅ Region participants check passed.")
    
    # Check if total girls and boys match their specific groups (yerevan + region)
    total_girls_check = statistics["girl_yerevan_participants"] + statistics["girl_region_participants"]
    if total_girls_check != statistics["girl_participants"]:
        print(f"❌ Total girls mismatch! {total_girls_check} != {statistics['girl_participants']}")
    else:
        print("✅ Total girls check passed.")

    total_boys_check = statistics["boy_yerevan_participants"] + statistics["boy_region_participants"]
    if total_boys_check != statistics["boy_participants"]:
        print(f"❌ Total boys mismatch! {total_boys_check} != {statistics['boy_participants']}")
    else:
        print("✅ Total boys check passed.")
    
    # Check if each region's participant count is consistent
    for region in armenia_regions_latins.values():
        total_region_participants = statistics.get(f"total_{region}_participants", 0)
        girl_region_participants = statistics.get(f"girl_{region}_participants", 0)
        boy_region_participants = statistics.get(f"boy_{region}_participants", 0)
        if total_region_participants != (girl_region_participants + boy_region_participants):
            print(f"❌ Region {region} participants mismatch! {girl_region_participants} + {boy_region_participants} != {total_region_participants}")
        else:
            print(f"✅ Region {region} participants check passed.")

    # Check if the unclassified participants count matches the overall unclassified count
    total_unclassified = sum(1 for value in statistics.values() if value == "unclassified")
    if total_unclassified != statistics["unclassified_participants"]:
        print(f"❌ Unclassified participants mismatch! {total_unclassified} != {statistics['unclassified_participants']}")
    else:
        print("✅ Unclassified participants check passed.")
    
    # Check subject participants (ensure consistency for subjects like armenian25, chemistry25, etc.)
    total_subject_participants = sum([statistics.get(f"{subject}_participants", 0) for subject in ["armenian25", "chemistry25", "history25", "english25", "physics25", "math25"]])
    if total_subject_participants != statistics["total_participants"]:
        print(f"❌ Subject participants mismatch! {total_subject_participants} != {statistics['total_participants']}")
    else:
        print("✅ Subject participants check passed.")


