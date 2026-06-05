// ১. লিঙ্কগুলো জমা রাখার জন্য একটি খালি সেট (Set) তৈরি করা হলো
if (typeof savedLinksSet === 'undefined') {
    var savedLinksSet = new Set();
} else {
    savedLinksSet.clear();
}

console.log("자동 স্ক্রলিং এবং লিঙ্ক কালেক্ট করা শুরু হলো...");

// ২. স্ক্রল করার এবং প্রতিবার নতুন লিঙ্ক জমা করার ফাংশন
const collectAndScroll = setInterval(() => {
    // বর্তমান স্ক্রিনে থাকা সব লিঙ্ক খুঁজে বের করা
    const currentLinks = Array.from(document.querySelectorAll('a[href*="/reels/"], a[href*="/p/"]'));
    currentLinks.forEach(a => savedLinksSet.add(a.href));
    
    console.log(`বর্তমানে মোট জমানো ইউনিক লিঙ্ক: ${savedLinksSet.size} টি`);

    // নিচের দিকে স্ক্রল করা
    window.scrollTo(0, document.body.scrollHeight);
}, 2000); // প্রতি ২ সেকেন্ড পর পর স্ক্রল হবে

// ৩. স্ক্রলিং বন্ধ করার এবং ফাইল ডাউনলোড করার ফাংশন
function stopAndDownload() {
    clearInterval(collectAndScroll);
    const uniqueLinks = Array.from(savedLinksSet);
    
    if(uniqueLinks.length === 0) {
        console.log("কোনো লিঙ্ক পাওয়া যায়নি!");
        return;
    }

    let csvContent = "data:text/csv;charset=utf-8,ID,URL,Title,Hashtags\n";
    uniqueLinks.forEach((link, index) => {
        csvContent += `${index + 1},"${link}","",""\n`;
    });

    const encodedUri = encodeURI(csvContent);
    const downloadLink = document.createElement("a");
    downloadLink.setAttribute("href", encodedUri);
    downloadLink.setAttribute("download", "new_reels.csv");
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
    
    console.log(`সফলভাবে ${uniqueLinks.length} টি লিঙ্ক ডাউনলোড হয়েছে!`);
}
