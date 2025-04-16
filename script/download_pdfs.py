import os
import re
import requests
import pdfplumber
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Mapping from subject page to subfolder
subject_pages = {
    "https://olymp.am/hy/node/1141": "math25",
    "https://olymp.am/hy/node/1175": "physics25",
    "https://olymp.am/hy/node/1164": "armenian25",
    "https://olymp.am/hy/node/1226": "english25",
    "https://olymp.am/hy/node/1220": "history25",
    "https://olymp.am/hy/node/1166": "chemistry25"
}

# Base directories
data_pdf_base = "/home/student/Desktop/Statistics Project/data/data_pdf"
data_csv_base = "/home/student/Desktop/Statistics Project/data/data_csv"

# Ensure base folders exist
os.makedirs(data_pdf_base, exist_ok=True)
os.makedirs(data_csv_base, exist_ok=True)

# Step 1: Download PDFs into subfolders
for url, subject in subject_pages.items():
    subject_pdf_dir = os.path.join(data_pdf_base, subject)
    os.makedirs(subject_pdf_dir, exist_ok=True)

    print(f"\n📄 Scraping PDF links for: {subject}")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch {url}: {e}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    pdf_links = [
        urljoin(url, a["href"]) for a in soup.find_all("a", href=True)
        if a["href"].lower().endswith(".pdf")
    ]

    for pdf_url in pdf_links:
        filename = os.path.basename(pdf_url)
        save_path = os.path.join(subject_pdf_dir, filename)

        if not os.path.exists(save_path):
            print(f"⬇️  Downloading {filename}...")
            try:
                pdf_response = requests.get(pdf_url)
                pdf_response.raise_for_status()
                with open(save_path, "wb") as f:
                    f.write(pdf_response.content)
                print(f"✅ Saved to {save_path}")
            except Exception as e:
                print(f"❌ Failed to download {pdf_url}: {e}")
        else:
            print(f"⚠️  {filename} already exists. Skipping.")

# Step 2: Convert PDFs to CSVs in matching subfolders
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
