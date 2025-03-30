import json
from os import listdir, rename

with open("series.json", "r", encoding="utf-8") as f:
    data = json.load(f)
data = data["nodes"]

for pdf in listdir("pdfs"):
    matches = []
    for book in data:
        names = [word.strip(".").strip("!").lower() for word in book["title"].split(" ")]
        if sum([+(word in pdf.lower()) for word in names]) > 0.5 * len(names):
            matches.append(book)
    if len(matches) == 1:
        match = matches[0]
    elif len(matches) > 1:
        print(f"Help match book {pdf}")
        print("\n".join([str(book) for book in matches]))
        val = None
        match = None
        while (val is None) or (match is None):
            try:
                val = int(input("Enter number (from 0 index) of correct book choice: "))
                match = matches[val]
            except ValueError:
                pass
            except IndexError:
                pass
        print(f"Selected book {match}")
    else:
        print(f"No match found for book {pdf}")
        print(f"Help match book {pdf}")
        print("\n".join([str(book) for book in data]))
        val = None
        match = None
        while (val is None) or (match is None):
            try:
                val = int(input("Enter number (from 0 index) of correct book choice: "))
                match = data[val]
            except ValueError:
                pass
            except IndexError:
                pass
        print(f"Selected book {match}")
    match['title'] = "".join([char for char in match['title'] if char.lower() in "qwertyuiopasdfghjklzxcvbnm -1234567890"])
    rename(f"pdfs/{pdf}", f"pdfs/{match['id']}- {match['title']}.pdf")
    print(f"{pdf} to book '{match['id']}- {match['title']}.pdf'")