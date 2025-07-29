import feedparser
import json
import os
import subprocess
import platform

SOURCES_FILE = "feeds.json"
READ_FILE = "read.json"

def load_sources():
    if not os.path.exists(SOURCES_FILE):
        return []
    with open(SOURCES_FILE, "r") as f:
        return json.load(f)

def load_read():
    if not os.path.exists(READ_FILE):
        return []
    with open(READ_FILE, "r") as f:
        return json.load(f)

def save_read(read_list):
    with open(READ_FILE, "w") as f:
        json.dump(read_list, f, indent=2)

def fetch_feed(url):
    feed = feedparser.parse(url)
    return feed.entries[:5]

def show_feeds():
    sources = load_sources()
    read = load_read()
    articles = []

    if not sources:
        print("No RSS feeds exist.")
        return articles

    count = 1
    for url in sources:
        print(f"\n🔗 {url}")
        try:
            entries = fetch_feed(url)
            for entry in entries:
                is_read = entry.link in read
                status = "✅" if is_read else "🔸"
                print(f"{count:02d}. {status} {entry.title}")
                print(f"    {entry.link}")
                articles.append(entry.link)
                count += 1
        except Exception as e:
            print(f"Error: {e}")

    return articles

def open_article(articles, index):
    try:
        link = articles[index - 1]
        system = platform.system()
        if system == "Darwin":  # macOS
            subprocess.run(["open", link], check=False)
        elif system == "Windows":
            subprocess.run(["start", link], shell=True, check=False)
        else:  # Linux ve diğerleri
            subprocess.run(["xdg-open", link], check=False)
        
        read = load_read()
        if link not in read:
            read.append(link)
            save_read(read)
            print("📖 Marked as read.")
    except IndexError:
        print("❌ Invalid article number.")


if __name__ == "__main__":
    all_articles = show_feeds()
    if all_articles:
        choice = input("\n📥 Article number: ")
        if choice.strip().isdigit():
            open_article(all_articles, int(choice.strip()))
