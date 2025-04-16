import os
import pandas as pd

# Folder containing CSVs
csv_dir = "/home/student/Desktop/Statistics Project/data/data_csv"

# Set to store unique names
unique_names = set()

# Loop over each CSV file
for root, dirs, files in os.walk(csv_dir):
    for file in files:
        if file.endswith(".csv"):
            filepath = os.path.join(root, file)
            try:
                df = pd.read_csv(filepath)
                if 'name' in df.columns:
                    unique_names.update(df['name'].dropna().unique())
                else:
                    print(f"⚠️ No 'name' column in {file}")
            except Exception as e:
                print(f"❌ Failed to process {file}: {e}")

# Sort and display
unique_names = sorted(unique_names)
print(f"\n✅ Found {len(unique_names)} unique names.\n")
for name in unique_names:
    print(name)

# Save to file
with open("unique_names.txt", "w", encoding="utf-8") as f:
    for name in unique_names:
        f.write(name + "\n")

print("\n📝 Saved to unique_names.txt")
