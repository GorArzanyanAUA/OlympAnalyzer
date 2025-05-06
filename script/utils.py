import os
import pandas as pd
import json

# Dictionary mapping Armenian region names to their Latin equivalents
armenia_regions_latins = {
    "Երևան": "Yerevan",
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

def calculate_statistics(data_csv_base, armenia_regions_latins):

    statistics = {
        "total_participants": 0,
        "girl_participants": 0,
        "boy_participants": 0,
        "unclassified_participants": 0,  # Unclassified participants
    }

    # Initialize dictionary to track region-wise statistics using Latin names
    region_counts = {latin_name: {"total": 0, "girl": 0, "boy": 0} for latin_name in armenia_regions_latins.values()}
    
    # Initialize dictionary to track participants per subject
    subject_participants = {}

    # Initialize dictionary to track gender distribution per subject per region
    subject_region_gender_distribution = {
        subject: {region: {"girl": 0, "boy": 0} for region in armenia_regions_latins.values()}
        for subject in ["armenian25", "chemistry25", "english25", "history25", "math25", "physics25"]
    }

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

                    if 'gender' in df.columns and 'region' in df.columns:
                        for _, row in df.iterrows():
                            gender = row['gender'].lower() if pd.notna(row['gender']) else None
                            region = row['region'] if pd.notna(row['region']) else None

                            # Total participants
                            statistics["total_participants"] += 1
                            subject_participants[subject] += 1  # Increment the subject participant count

                            if region in armenia_regions_latins:
                                latin_region = armenia_regions_latins.get(region, region)  # Get the Latin name for the region
                                region_counts[latin_region]["total"] += 1
                            else:
                                statistics["unclassified_participants"] += 1  # Unclassified participants

                            # Classify by gender
                            if gender == "girl":
                                statistics["girl_participants"] += 1
                                if region in armenia_regions_latins:
                                    latin_region = armenia_regions_latins.get(region, region)  # Get the Latin name for the region
                                    region_counts[latin_region]["girl"] += 1
                                    subject_region_gender_distribution[subject][latin_region]["girl"] += 1
                            elif gender == "boy":
                                statistics["boy_participants"] += 1
                                if region in armenia_regions_latins:
                                    latin_region = armenia_regions_latins.get(region, region)  # Get the Latin name for the region
                                    region_counts[latin_region]["boy"] += 1
                                    subject_region_gender_distribution[subject][latin_region]["boy"] += 1
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

    # # Add region_gender statistics to the main statistics dictionary
    # for region_gender, count in region_gender_counts.items():
    #     statistics[region_gender] = count

    # Add subject statistics to the main statistics dictionary
    for subject, count in subject_participants.items():
        statistics[f"{subject}_participants"] = count

    # Add subject region-gender statistics to the main statistics dictionary
    for subject, region_data in subject_region_gender_distribution.items():
        for region, gender_data in region_data.items():
            statistics[f"{subject}_{region}_girl"] = gender_data["girl"]
            statistics[f"{subject}_{region}_boy"] = gender_data["boy"]

    # Save the calculated statistics to a new JSON file
    output_folder = "/home/student/Desktop/Statistics Project/analyses/"
    output_file = "calculated_statistics_with_subject_region_gender.json"
    with open(output_folder + output_file, "w") as f:
        json.dump(statistics, f, indent=4)

    print(f"✅ Statistics calculated and saved to {output_file}")
    return statistics

def second_calculate_statistics(data_csv_base, armenia_regions_latins):

    statistics = {
        "total_participants": 0,
        "girl_participants": 0,
        "boy_participants": 0,
        "unclassified_participants": 0,  # Unclassified participants
    }

    # Initialize dictionary to track region-wise statistics using Latin names
    region_counts = {latin_name: {"total": 0, "girl": 0, "boy": 0} for latin_name in armenia_regions_latins.values()}
    
    # Initialize dictionary to track participants per subject
    subject_participants = {}

    # Initialize dictionary to track gender distribution per subject per region
    subject_region_gender_distribution = {
        subject: {region: {"girl": 0, "boy": 0} for region in armenia_regions_latins.values()}
        for subject in ["armenian25", "chemistry25", "english25", "history25", "math25", "physics25"]
    }

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

                    if 'gender' in df.columns and 'region' in df.columns:
                        for _, row in df.iterrows():
                            gender = row['gender'].lower() if pd.notna(row['gender']) else None
                            region = row['region'] if pd.notna(row['region']) else None
                            current_region = None
                            # Total participants
                            statistics["total_participants"] += 1
                            subject_participants[subject] += 1  # Increment the subject participant count

                            if region in armenia_regions_latins:
                                latin_region = armenia_regions_latins.get(region, region)  # Get the Latin name for the region
                                region_counts[latin_region]["total"] += 1
                            else:
                                statistics["unclassified_participants"] += 1
                                statistics["total_participants"] -= 1
                                subject_participants[subject] -= 1
                                print("unclassified region")
                                continue
                      
                            # Classify by gender
                            if gender == "girl":
                                statistics["girl_participants"] += 1
                                if region in armenia_regions_latins:
                                    latin_region = armenia_regions_latins.get(region, region)  # Get the Latin name for the region
                                    region_counts[latin_region]["girl"] += 1
                                    subject_region_gender_distribution[subject][latin_region]["girl"] += 1
                            
                            elif gender == "boy":
                                statistics["boy_participants"] += 1
                                if region in armenia_regions_latins:
                                    latin_region = armenia_regions_latins.get(region, region)  # Get the Latin name for the region
                                    region_counts[latin_region]["boy"] += 1
                                    subject_region_gender_distribution[subject][latin_region]["boy"] += 1
                            else:
                                statistics["unclassified_participants"] += 1  # Unclassified participants
                                statistics["total_participants"] -= 1
                                subject_participants[subject] -= 1
                    else:
                        print(f"⚠️ Skipped: Missing 'gender' or 'region' column in {file}")

                except Exception as e:
                    print(f"❌ Error processing {file}: {e}")



    # Add region-wise statistics to the main statistics dictionary
    for region, counts in region_counts.items():
        statistics[f"total_{region}_participants"] = counts["total"]
        statistics[f"girl_{region}_participants"] = counts["girl"]
        statistics[f"boy_{region}_participants"] = counts["boy"]
        assert counts["total"] == counts["girl"] + counts["boy"]

    # # Add region_gender statistics to the main statistics dictionary
    # for region_gender, count in region_gender_counts.items():
    #     statistics[region_gender] = count

    _sub_total_participants = 0
    # Add subject statistics to the main statistics dictionary
    for subject, count in subject_participants.items():
        statistics[f"{subject}_participants"] = count
        _sub_total_participants += count
    assert _sub_total_participants == statistics["total_participants"]

    # Add subject region-gender statistics to the main statistics dictionary
    for subject, region_data in subject_region_gender_distribution.items():
        _subject_total_participants = 0
        for region, gender_data in region_data.items():
            statistics[f"{subject}_{region}_girl"] = gender_data["girl"]
            statistics[f"{subject}_{region}_boy"] = gender_data["boy"]
            _subject_total_participants += gender_data["girl"] + gender_data["boy"]
        assert _subject_total_participants == statistics[f"{subject}_participants"]


    # Save the calculated statistics to a new JSON file
    output_folder = "/home/student/Desktop/Statistics Project/analyses/"
    output_file = "second_calculated_statistics_with_subject_region_gender.json"
    with open(output_folder + output_file, "w") as f:
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

def check_data_consistency_updated(statistics, armenia_regions_latins):
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
    
    # Check subject-region-gender participants (new check for gender distribution in subjects per region)
    for subject in ["armenian25", "chemistry25", "history25", "english25", "physics25", "math25"]:
        for region in armenia_regions_latins.values():
            girl_count = statistics.get(f"{subject}_{region}_girl", 0)
            boy_count = statistics.get(f"{subject}_{region}_boy", 0)
            total_subject_region_gender = girl_count + boy_count
            total_subject_region_participants = statistics.get(f"{subject}_{region}_participants", 0)
            
            if total_subject_region_gender != total_subject_region_participants:
                print(f"❌ Subject {subject} in Region {region} gender mismatch! {girl_count} + {boy_count} != {total_subject_region_participants}")
            else:
                print(f"✅ Subject {subject} in Region {region} gender check passed.")


# check_data_consistency(statistics)

second_calculate_statistics("/home/student/Desktop/Statistics Project/data/data_csv", armenia_regions_latins)

stat2 = {
    "total_participants": 60120,
    "yerevan_participants": 16310,
    "region_participants": 43601,
    "girl_participants": 35830,
    "boy_participants": 24290,
    "girl_yerevan_participants": 8358,
    "girl_region_participants": 27368,
    "boy_yerevan_participants": 7952,
    "boy_region_participants": 16233,
    "unclassified_participants": 175,
    "total_Ararat_participants": 4868,
    "girl_Ararat_participants": 3063,
    "boy_Ararat_participants": 1800,
    "total_Aragatsotn_participants": 3039,
    "girl_Aragatsotn_participants": 1913,
    "boy_Aragatsotn_participants": 1125,
    "total_Gegharkunik_participants": 4863,
    "girl_Gegharkunik_participants": 3126,
    "boy_Gegharkunik_participants": 1736,
    "total_Kotayk_participants": 7074,
    "girl_Kotayk_participants": 4527,
    "boy_Kotayk_participants": 2546,
    "total_Lori_participants": 5522,
    "girl_Lori_participants": 3420,
    "boy_Lori_participants": 2096,
    "total_Shirak_participants": 5155,
    "girl_Shirak_participants": 3159,
    "boy_Shirak_participants": 1990,
    "total_Syunik_participants": 4015,
    "girl_Syunik_participants": 2390,
    "boy_Syunik_participants": 1624,
    "total_Vayots Dzor_participants": 1517,
    "girl_Vayots Dzor_participants": 973,
    "boy_Vayots Dzor_participants": 544,
    "total_Tavush_participants": 3020,
    "girl_Tavush_participants": 1889,
    "boy_Tavush_participants": 1125,
    "total_Armavir_participants": 4562,
    "girl_Armavir_participants": 2908,
    "boy_Armavir_participants": 1647,
    "Ararat_girl": 3063,
    "Aragatsotn_girl": 1913,
    "Gegharkunik_girl": 3126,
    "Kotayk_girl": 4527,
    "Lori_girl": 3420,
    "Shirak_girl": 3159,
    "Syunik_girl": 2390,
    "Vayots Dzor_girl": 973,
    "Tavush_girl": 1889,
    "Armavir_girl": 2908,
    "Ararat_boy": 1800,
    "Aragatsotn_boy": 1125,
    "Gegharkunik_boy": 1736,
    "Kotayk_boy": 2546,
    "Lori_boy": 2096,
    "Shirak_boy": 1990,
    "Syunik_boy": 1624,
    "Vayots Dzor_boy": 544,
    "Tavush_boy": 1125,
    "Armavir_boy": 1647,
    "armenian25_participants": 9166,
    "chemistry25_participants": 2531,
    "history25_participants": 5201,
    "english25_participants": 7626,
    "physics25_participants": 3513,
    "math25_participants": 32083,
    "armenian25_Ararat_girl": 813,
    "armenian25_Ararat_boy": 143,
    "armenian25_Aragatsotn_girl": 449,
    "armenian25_Aragatsotn_boy": 93,
    "armenian25_Gegharkunik_girl": 727,
    "armenian25_Gegharkunik_boy": 155,
    "armenian25_Kotayk_girl": 883,
    "armenian25_Kotayk_boy": 172,
    "armenian25_Lori_girl": 693,
    "armenian25_Lori_boy": 141,
    "armenian25_Shirak_girl": 750,
    "armenian25_Shirak_boy": 190,
    "armenian25_Syunik_girl": 529,
    "armenian25_Syunik_boy": 124,
    "armenian25_Vayots Dzor_girl": 237,
    "armenian25_Vayots Dzor_boy": 63,
    "armenian25_Tavush_girl": 517,
    "armenian25_Tavush_boy": 105,
    "armenian25_Armavir_girl": 553,
    "armenian25_Armavir_boy": 114,
    "chemistry25_Ararat_girl": 210,
    "chemistry25_Ararat_boy": 72,
    "chemistry25_Aragatsotn_girl": 97,
    "chemistry25_Aragatsotn_boy": 40,
    "chemistry25_Gegharkunik_girl": 196,
    "chemistry25_Gegharkunik_boy": 55,
    "chemistry25_Kotayk_girl": 216,
    "chemistry25_Kotayk_boy": 80,
    "chemistry25_Lori_girl": 135,
    "chemistry25_Lori_boy": 68,
    "chemistry25_Shirak_girl": 192,
    "chemistry25_Shirak_boy": 80,
    "chemistry25_Syunik_girl": 107,
    "chemistry25_Syunik_boy": 52,
    "chemistry25_Vayots Dzor_girl": 68,
    "chemistry25_Vayots Dzor_boy": 21,
    "chemistry25_Tavush_girl": 105,
    "chemistry25_Tavush_boy": 44,
    "chemistry25_Armavir_girl": 158,
    "chemistry25_Armavir_boy": 51,
    "english25_Ararat_girl": 568,
    "english25_Ararat_boy": 157,
    "english25_Aragatsotn_girl": 225,
    "english25_Aragatsotn_boy": 72,
    "english25_Gegharkunik_girl": 318,
    "english25_Gegharkunik_boy": 96,
    "english25_Kotayk_girl": 1151,
    "english25_Kotayk_boy": 338,
    "english25_Lori_girl": 456,
    "english25_Lori_boy": 172,
    "english25_Shirak_girl": 352,
    "english25_Shirak_boy": 146,
    "english25_Syunik_girl": 383,
    "english25_Syunik_boy": 129,
    "english25_Vayots Dzor_girl": 128,
    "english25_Vayots Dzor_boy": 41,
    "english25_Tavush_girl": 215,
    "english25_Tavush_boy": 57,
    "english25_Armavir_girl": 360,
    "english25_Armavir_boy": 118,
    "history25_Ararat_girl": 0,
    "history25_Ararat_boy": 0,
    "history25_Aragatsotn_girl": 236,
    "history25_Aragatsotn_boy": 97,
    "history25_Gegharkunik_girl": 481,
    "history25_Gegharkunik_boy": 181,
    "history25_Kotayk_girl": 405,
    "history25_Kotayk_boy": 165,
    "history25_Lori_girl": 371,
    "history25_Lori_boy": 170,
    "history25_Shirak_girl": 405,
    "history25_Shirak_boy": 137,
    "history25_Syunik_girl": 202,
    "history25_Syunik_boy": 95,
    "history25_Vayots Dzor_girl": 137,
    "history25_Vayots Dzor_boy": 54,
    "history25_Tavush_girl": 233,
    "history25_Tavush_boy": 98,
    "history25_Armavir_girl": 555,
    "history25_Armavir_boy": 229,
    "math25_Ararat_girl": 1305,
    "math25_Ararat_boy": 1293,
    "math25_Aragatsotn_girl": 823,
    "math25_Aragatsotn_boy": 764,
    "math25_Gegharkunik_girl": 1092,
    "math25_Gegharkunik_boy": 999,
    "math25_Kotayk_girl": 1718,
    "math25_Kotayk_boy": 1674,
    "math25_Lori_girl": 1605,
    "math25_Lori_boy": 1434,
    "math25_Shirak_girl": 1289,
    "math25_Shirak_boy": 1296,
    "math25_Syunik_girl": 1090,
    "math25_Syunik_boy": 1127,
    "math25_Vayots Dzor_girl": 354,
    "math25_Vayots Dzor_boy": 333,
    "math25_Tavush_girl": 738,
    "math25_Tavush_boy": 749,
    "math25_Armavir_girl": 1143,
    "math25_Armavir_boy": 1037,
    "physics25_Ararat_girl": 167,
    "physics25_Ararat_boy": 135,
    "physics25_Aragatsotn_girl": 83,
    "physics25_Aragatsotn_boy": 59,
    "physics25_Gegharkunik_girl": 312,
    "physics25_Gegharkunik_boy": 250,
    "physics25_Kotayk_girl": 154,
    "physics25_Kotayk_boy": 117,
    "physics25_Lori_girl": 160,
    "physics25_Lori_boy": 111,
    "physics25_Shirak_girl": 171,
    "physics25_Shirak_boy": 141,
    "physics25_Syunik_girl": 79,
    "physics25_Syunik_boy": 97,
    "physics25_Vayots Dzor_girl": 49,
    "physics25_Vayots Dzor_boy": 32,
    "physics25_Tavush_girl": 81,
    "physics25_Tavush_boy": 72,
    "physics25_Armavir_girl": 139,
    "physics25_Armavir_boy": 98
}
