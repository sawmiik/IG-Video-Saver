import csv
import os

# Define the file names
OLD_FILE = 'old_reels.csv'
NEW_FILE = 'new_reels.csv'
UPDATE_FILE = 'reels_to_add.csv'

def find_new_reels():
    print("Looking for new reels...")
    
    # 1. Read the old URLs into a list so we know what we already have
    old_urls = set()
    if os.path.exists(OLD_FILE):
        with open(OLD_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                old_urls.add(row['URL'])
    else:
        print(f"Error: {OLD_FILE} not found!")
        return

    # 2. Read the new file and keep ONLY the ones that aren't in the old file
    new_entries = []
    if os.path.exists(NEW_FILE):
        with open(NEW_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['URL'] not in old_urls:
                    new_entries.append(row)
    else:
        print(f"Error: {NEW_FILE} not found!")
        return

    # 3. Save the new entries to our 'Update' file
    if new_entries:
        with open(UPDATE_FILE, 'w', newline='', encoding='utf-8') as f:
            # Recreate the headers exactly as they are
            writer = csv.DictWriter(f, fieldnames=['ID', 'URL', 'Title', 'Hashtags'])
            writer.writeheader()
            writer.writerows(new_entries)
        print(f"Success! Found {len(new_entries)} new reels.")
        print(f"Saved them to '{UPDATE_FILE}'. Ready to import to Notion!")
    else:
        print("No new reels found. Your Notion database is already up to date.")

# Run the function
if __name__ == "__main__":
    find_new_reels()
    
