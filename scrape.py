import csv
import requests
from bs4 import BeautifulSoup

input_csv_path = 'links.csv'
output_csv_path = 'downloaded_content.csv'
progress_tracker_path = 'progress_tracker.txt'

def save_progress(last_row):
    with open(progress_tracker_path, 'w') as f:
        f.write(str(last_row))

def load_progress():
    try:
        with open(progress_tracker_path, 'r') as f:
            return int(f.read())
    except FileNotFoundError:
        return 0  # Start from the beginning if no progress file found

start_row = load_progress()

with open(input_csv_path, mode='r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    urls = list(reader)

with open(output_csv_path, mode='a', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    for index, row in enumerate(urls[start_row:], start=start_row):
        url = row[0]
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            body_content = soup.body.get_text(separator=' ', strip=True) if soup.body else ''
            
            # Exclude specified text and replace newlines and carriage returns
            exclude_text = "Date created:"
            if exclude_text in body_content:
                body_content = body_content.split(exclude_text)[0]
            
            clean_content = body_content.replace('\n', ' ').replace('\r', ' ').strip().rstrip("'").rstrip('"')
            
            writer.writerow([clean_content[:10000000]])  # Ensure the content is a single cell
            
            save_progress(index)
        except requests.RequestException as e:
            print(f"Error downloading {url}: {e}")
            save_progress(index)

print("Download completed.")
