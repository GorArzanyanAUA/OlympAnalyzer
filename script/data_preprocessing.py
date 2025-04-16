import os
import re
import requests
import pdfplumber
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from names import armenian_female_names, armenian_male_names
# ========== CONFIGURATION ==========
subject_pages = {
    "https://olymp.am/hy/node/1141": "math25",
    "https://olymp.am/hy/node/1175": "physics25",
    "https://olymp.am/hy/node/1164": "armenian25",
    "https://olymp.am/hy/node/1226": "english25",
    "https://olymp.am/hy/node/1220": "history25",
    "https://olymp.am/hy/node/1166": "chemistry25"
}

data_pdf_base = "/home/student/Desktop/Statistics Project/data/data_pdf"
data_csv_base = "/home/student/Desktop/Statistics Project/data/data_csv"


male_names = set(name.lower() for name in armenian_male_names)
female_names = set(name.lower() for name in armenian_female_names)

# ========== HELPER FUNCTIONS ==========
def classify_name(name):
    name = str(name).strip().lower()
    if name in female_names:
        return "girl"
    elif name in male_names:
        return "boy"
    else:
        return "unknown"

def download_pdfs():
    os.makedirs(data_pdf_base, exist_ok=True)
    for url, subject in subject_pages.items():
        subject_pdf_dir = os.path.join(data_pdf_base, subject)
        os.makedirs(subject_pdf_dir, exist_ok=True)
        print(f"\n📄 Scraping PDF links for: {subject}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            pdf_links = [
                urljoin(url, a["href"]) for a in soup.find_all("a", href=True)
                if a["href"].lower().endswith(".pdf")
            ]
            for pdf_url in pdf_links:
                filename = os.path.basename(pdf_url)
                save_path = os.path.join(subject_pdf_dir, filename)
                if not os.path.exists(save_path):
                    print(f"⬇️ Downloading {filename}...")
                    pdf_response = requests.get(pdf_url)
                    pdf_response.raise_for_status()
                    with open(save_path, "wb") as f:
                        f.write(pdf_response.content)
                    print(f"✅ Saved to {save_path}")
                else:
                    print(f"⚠️ {filename} already exists. Skipping.")
        except Exception as e:
            print(f"❌ Failed to fetch {url}: {e}")

def convert_pdfs_to_csv():
    os.makedirs(data_csv_base, exist_ok=True)
    for subject in os.listdir(data_pdf_base):
        subject_pdf_dir = os.path.join(data_pdf_base, subject)
        subject_csv_dir = os.path.join(data_csv_base, subject)
        os.makedirs(subject_csv_dir, exist_ok=True)
        for filename in os.listdir(subject_pdf_dir):
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(subject_pdf_dir, filename)
                csv_path = os.path.join(subject_csv_dir, os.path.splitext(filename)[0] + ".csv")
                data = []
                try:
                    with pdfplumber.open(pdf_path) as pdf:
                        for page in pdf.pages:
                            text = page.extract_text()
                            if not text:
                                continue
                            lines = text.split('\n')
                            for line in lines:
                                if re.match(r'^\d{6}', line):
                                    parts = line.strip().split()
                                    if len(parts) < 8:
                                        continue
                                    id_ = parts[0]
                                    surname = parts[1]
                                    name = parts[2]
                                    fathername = parts[3]
                                    grade = parts[4]
                                    region = parts[5]
                                    score = parts[-1]
                                    school = " ".join(parts[6:-1])
                                    data.append([id_, surname, name, fathername, grade, region, school, score])
                    df = pd.DataFrame(data, columns=['id', 'surname', 'name', 'fathername', 'grade', 'region', 'school', 'score'])
                    df.to_csv(csv_path, index=False)
                    print(f"📤 Converted to CSV: {csv_path}")
                except Exception as e:
                    print(f"❌ Error processing {pdf_path}: {e}")

def add_gender_and_filter_unknowns():
    all_unknown_rows = []
    unknown_name_set = set()

    for root, dirs, files in os.walk(data_csv_base):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                print(f"\n📄 Processing: {file}")
                try:
                    df = pd.read_csv(file_path)
                    if "name" in df.columns:
                        df["gender"] = df["name"].apply(classify_name)
                        unknown_df = df[df["gender"] == "unknown"].copy()
                        unknown_df["source_file"] = file
                        all_unknown_rows.append(unknown_df)
                        unknown_name_set.update(unknown_df["name"].dropna().unique())
                        df = df[df["gender"] != "unknown"]
                        df.to_csv(file_path, index=False)
                        print(f"✅ Updated {file} with gender column")
                        print(f"❓ Removed {len(unknown_df)} unknown entries")
                    else:
                        print("⚠️ Skipped: no 'name' column found")
                except Exception as e:
                    print(f"❌ Error processing {file}: {e}")

    if all_unknown_rows:
        all_unknowns_df = pd.concat(all_unknown_rows, ignore_index=True)
        all_unknowns_df.to_csv("unknown_samples.txt", index=False)
        print(f"\n🔍 Total unknown names: {len(all_unknowns_df)}")
        print("📝 Saved full unknown entries to 'unknown_samples.txt'")

        # Save just the unknown name list
        sorted_names = sorted(unknown_name_set)
        with open("unknown_names.txt", "w", encoding="utf-8") as f:
            for name in sorted_names:
                f.write(name + "\n")
        print(f"📝 Saved {len(sorted_names)} unique unknown names to 'unknown_names.txt'")
    else:
        print("\n🔍 No unknown names found across all files")

def collect_unique_names():
    unique_names = set()
    for root, dirs, files in os.walk(data_csv_base):
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
    unique_names = sorted(unique_names)
    with open("unique_names.txt", "w", encoding="utf-8") as f:
        for name in unique_names:
            f.write(name + "\n")
    print(f"\n✅ Found {len(unique_names)} unique names.")
    print("📝 Saved to 'unique_names.txt'")

# ========== MAIN FUNCTION ==========
def main():
    print("🚀 Starting data processing pipeline...\n")
    download_pdfs()
    convert_pdfs_to_csv()
    add_gender_and_filter_unknowns()
    collect_unique_names()
    print("\n✅ All steps completed!")

if __name__ == "__main__":
    main()
