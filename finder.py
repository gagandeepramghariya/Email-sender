import requests
from bs4 import BeautifulSoup
import re
import csv
import time
import os
from urllib.parse import urljoin
#seo agency New York

# 🔐 API KEY (set in terminal: export SERPAPI_KEY="your_key")
API_KEY = os.getenv("SERPAPI_KEY")

query = input("🔍 Search (example: 3d animation studio USA): ")

# 🌐 Get websites from Google Maps
def get_maps_data(query, total_results=100):
    url = "https://serpapi.com/search.json"
    all_websites = set()

    for start in range(0, total_results, 20):  # 20 results per page
        params = {
            "engine": "google_maps",
            "q": query,
            "api_key": API_KEY,
            "start": start
        }

        try:
            res = requests.get(url, params=params)
            data = res.json()

            if "local_results" in data:
                for place in data["local_results"]:
                    if "website" in place:
                        all_websites.add(place["website"])

            print(f"📄 Page {start//20 + 1} done")

            time.sleep(2)

        except Exception as e:
            print("❌ API Error:", e)

    return list(all_websites)

# 📧 Extract emails
def extract_emails(url):
    emails = set()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        text = soup.get_text()

        found = re.findall(
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}", text
        )

        emails.update(found)

        # 🔥 Important pages scan
        pages = ["/contact", "/contact-us", "/about", "/support"]

        for link in pages:
            try:
                full_url = urljoin(url, link)
                res2 = requests.get(full_url, headers=headers, timeout=5)

                found2 = re.findall(
                    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}",
                    res2.text
                )

                emails.update(found2)

            except Exception as e:
                print(f"⚠️ Error in subpage {link}: {e}")

    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")

    return clean_emails(emails)


# 🧹 Clean emails (remove junk)
def clean_emails(email_set):
    clean = set()

    for email in email_set:
        if not any(x in email for x in ["example", "test", "yourdomain"]):
            clean.add(email.lower())

    return clean


# 🚀 MAIN
websites = get_maps_data(query)

print("\n🌐 Found Websites:", len(websites))

all_data = set()

for site in websites:
    print(f"🔎 Checking: {site}")

    emails = extract_emails(site)

    if emails:
        for email in emails:
            all_data.add((site, email))
    else:
        print("⚠️ No email found")

    time.sleep(2)  # avoid blocking


# 💾 Save CSV
with open("clients.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Website", "Email"])

    for row in all_data:
        writer.writerow(row)

print(f"\n✅ Done! {len(all_data)} emails saved in clients.csv")
print("API KEY:", API_KEY)