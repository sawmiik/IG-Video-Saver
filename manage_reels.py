import csv
import os

# ফাইলের নামগুলো ডিফাইন করা হলো
OLD_FILE = 'old_reels.csv'
NEW_FILE = 'new_reels.csv'
UPDATE_FILE = 'reels_to_add.csv'
PROCESSED_FILE = 'processed_new_reels.csv' # নাম পরিবর্তনের পর নতুন নাম

def process_and_merge_reels():
    print("--------------------------------------------------")
    print("🔄 রিলস প্রসেসিং এবং ডাটাবেজ আপডেট শুরু হচ্ছে...")
    print("--------------------------------------------------")
    
    # === 🌟 এক্সট্রা সিকিউরিটি চেক ===
    # যদি আগের প্রসেস করা ফাইল থেকে থাকে, নতুন কাজের সুবিধার জন্য সেটি আগে রিমুভ করা হবে
    if os.path.exists(PROCESSED_FILE):
        try:
            os.remove(PROCESSED_FILE)
        except Exception:
            pass

    # === ">ধাপ ১: আগের ব্যাকআপ থেকে পুরোনো URL গুলো রিড করা ===
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
        print(f"✅ পুরাতন ডাটাবেজে {len(old_rows)} টি রিলস পাওয়া গেছে। (সর্বশেষ ID: {last_id})")
    else:
        print(f"ℹ️ {OLD_FILE} পাওয়া যায়নি। একটি নতুন ডাটাবেজ ফাইল তৈরি করা হবে।")

    # === ধাপ ২: নতুন স্ক্র্যাপ করা ফাইল থেকে শুধুমাত্র একদম নতুন রিলসগুলো খুঁজে বের করা ===
    new_entries = []
    
    if os.path.exists(NEW_FILE):
        with open(NEW_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # যদি লিঙ্কটি আগে সেভ করা না থাকে, তবেই এটি নতুন
                if row['URL'] not in old_urls:
                    last_id += 1 # আইডি ১ বাড়িয়ে দেওয়া হলো
                    new_row = {
                        'ID': str(last_id),
                        'URL': row['URL'],
                        'Title': '',
                        'Hashtags': ''
                    }
                    new_entries.append(new_row)
                    old_rows.append(new_row) # ভবিষ্যতের জন্য মেইন লিস্টে যোগ করা হলো
    else:
        print(f"❌ ভুল: ব্রাউজার থেকে ডাউনলোড করা '{NEW_FILE}' ফাইলটি ফোল্ডারে পাওয়া যায়নি!")
        return

    # === ধাপ ৩: নোশনে আপলোড করার জন্য শুধু নতুন রিলসের ফাইল (reels_to_add.csv) তৈরি ===
    if new_entries:
        with open(UPDATE_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['ID', 'URL', 'Title', 'Hashtags'])
            writer.writeheader()
            writer.writerows(new_entries)
        print(f"🎯 সফলভাবে {len(new_entries)} টি নতুন রিলস সনাক্ত করা হয়েছে!")
        print(f"📂 নোশনে ইম্পোর্ট করার ফাইলটি তৈরি: '{UPDATE_FILE}'")
        
        # === ">ধাপ ৪: স্বয়ংক্রিয়ভাবে মেইন ডাটাবেজ ফাইল (old_reels.csv) আপডেট ও মার্জ করা ===
        with open(OLD_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['ID', 'URL', 'Title', 'Hashtags'])
            writer.writeheader()
            writer.writerows(old_rows)
        print(f"💾 আপনার প্রধান ব্যাকআপ ফাইল '{OLD_FILE}' স্বয়ংক্রিয়ভাবে আপডেট করা হয়েছে। (মোট রিলস: {len(old_rows)} টি)")
        
        # === 🔄 ধাপ ৫: নাম পরিবর্তন (Rename) করে নির্দেশ করা যে কাজ শেষ ===
        try:
            os.rename(NEW_FILE, PROCESSED_FILE)
            print(f"📝 কাজ শেষ! '{NEW_FILE}' এর নাম পরিবর্তন করে রাখা হয়েছে: '{PROCESSED_FILE}'")
        except Exception as e:
            print(f"⚠️ ফাইলের নাম পরিবর্তনে সমস্যা হয়েছে: {e}")
            
    else:
        print("🎉 কোনো নতুন রিলস পাওয়া যায়নি! আপনার ডাটাবেজ অলরেডি আপ-টু-ডেট আছে।")
        # যদি কোনো নতুন রিলস নাও থাকে, তবুও ফাইলটি প্রসেসড হিসেবে রিনেম করে দেওয়া হবে
        try:
            os.rename(NEW_FILE, PROCESSED_FILE)
            print(f"📝 কোনো নতুন রিলস ছিল না, তবুও ফাইলের নাম বদলে রাখা হয়েছে: '{PROCESSED_FILE}'")
        except Exception:
            pass
        
    print("--------------------------------------------------")
    print("✨ সমস্ত প্রক্রিয়া সফলভাবে সম্পন্ন হয়েছে! ✨")
    print("--------------------------------------------------")

if __name__ == "__main__":
    process_and_merge_reels()
