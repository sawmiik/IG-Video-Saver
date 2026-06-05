import csv
import os

# Defining the file names
OLD_FILE = 'old_reels.csv'
NEW_FILE = 'new_reels.csv'
UPDATE_FILE = 'reels_to_add.csv'
PROCESSED_FILE = 'already_taken_from_here.csv' # Updated processed file name

def process_and_merge_reels():
    print("--------------------------------------------------")
    print("🔄 Starting Reels Processing & Database Update...")
    print("--------------------------------------------------")
    
    # === Extra Security Check ===
    # If a previously processed file exists, remove it first for the new session
    if os.path.exists(PROCESSED_FILE):
        try:
            os.remove(PROCESSED_FILE)
        except Exception:
            pass

    # === Step 1: Read existing URLs from the old backup database ===
    old_urls = set()
    old_rows = []
    last_id = 0
    
    if os.path.exists(OLD_FILE):
        with open(OLD_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                old_urls.add(row['URL'])
                old_rows.append(row)
                last_id = int(row['ID'])
        print(f"✅ Found {len(old_rows)} reels in the existing database. (Last ID: {last_id})")
    else:
        print(f"ℹ️ '{OLD_FILE}' not found. A new database file will be created.")

    # === Step 2: Read new scraped file and filter out unique new reels ===
    new_entries = []
    
    if os.path.exists(NEW_FILE):
        with open(NEW_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # If the URL is not in old_urls, then it's a completely new reel
                if row['URL'] not in old_urls:
                    last_id += 1 # Incrementing the ID by 1
                    new_row = {
                        'ID': str(last_id),
                        'URL': row['URL'],
                        'Title': '',
                        'Hashtags': ''
                    }
                    new_entries.append(new_row)
                    old_rows.append(new_row) # Appending to the main list for future updates
    else:
        print(f"❌ Error: Scraped file '{NEW_FILE}' was not found in this folder!")
        return

    # === Step 3: Create the file containing ONLY new reels for Notion import ===
    if new_entries:
        with open(UPDATE_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['ID', 'URL', 'Title', 'Hashtags'])
            writer.writeheader()
            writer.writerows(new_entries)
        print(f"🎯 Successfully identified {len(new_entries)} new reels!")
        print(f"📂 Notion import file created: '{UPDATE_FILE}'")
        
        # === Step 4: Automatically update and merge the main database file ===
        with open(OLD_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['ID', 'URL', 'Title', 'Hashtags'])
            writer.writeheader()
            writer.writerows(old_rows)
        print(f"💾 Main backup file '{OLD_FILE}' has been updated. (Total Reels: {len(old_rows)})")
        
        # === Step 5: Rename the new file to indicate it has been processed ===
        try:
            os.rename(NEW_FILE, PROCESSED_FILE)
            print(f"📝 Done! '{NEW_FILE}' has been renamed to: '{PROCESSED_FILE}'")
        except Exception as e:
            print(f"⚠️ Failed to rename the file: {e}")
            
    else:
        print("🎉 No new reels found! Your database is already up to date.")
        # Even if there are no new reels, rename the file to indicate it was processed
        try:
            os.rename(NEW_FILE, PROCESSED_FILE)
            print(f"📝 No new reels were present, but file was renamed to: '{PROCESSED_FILE}'")
        except Exception:
            pass
        
    print("--------------------------------------------------")
    print("✨ All processes completed successfully! ✨")
    print("--------------------------------------------------")

if __name__ == "__main__":
    process_and_merge_reels()
