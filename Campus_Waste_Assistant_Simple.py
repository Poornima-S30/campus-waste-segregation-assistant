"""
Campus Waste Segregation Assistant
Simple one-file version
Run this file directly in Python IDLE.
"""

import json
import os
from datetime import datetime

# ---------------- WASTE DATABASE ----------------

WASTE_DB = {
    "banana peel": ("Organic", "Green / Organic Collection",
                    "Place it in the organic or compostable waste collection according to campus rules.",
                    "Organic waste can be composted where facilities are available."),
    "fruit peel": ("Organic", "Green / Organic Collection",
                   "Dispose in the organic/compostable bin.",
                   "Fruit peels break down quickly and make good compost."),
    "food scraps": ("Organic", "Green / Organic Collection",
                    "Dispose in the organic/compostable bin.",
                    "Avoid mixing food scraps with packaging materials."),
    "leaves": ("Organic", "Green / Organic Collection",
               "Dispose in the organic/compostable bin or garden waste point.",
               "Dry leaves can be composted separately from wet waste."),
    "tea bags": ("Organic", "Green / Organic Collection",
                 "Dispose in the organic/compostable bin.",
                 "Check if the tea bag has a plastic lining before composting."),

    "paper": ("Recyclable", "Blue / Recycling Collection",
              "Place in the recycling collection, flattened if possible.",
              "Keep paper dry and clean to keep it recyclable."),
    "cardboard": ("Recyclable", "Blue / Recycling Collection",
                  "Flatten and place in the recycling collection.",
                  "Remove tape and labels from cardboard before recycling."),
    "newspaper": ("Recyclable", "Blue / Recycling Collection",
                  "Place in the recycling collection.",
                  "Bundle newspapers together to make collection easier."),
    "plastic bottle": ("Recyclable", "Blue / Recycling Collection",
                       "Empty and rinse the bottle, then place it in the recycling collection.",
                       "Crush bottles to save space in the recycling bin."),
    "bottle": ("Recyclable", "Blue / Recycling Collection",
               "Empty and rinse before placing in the recycling collection.",
               "Check the material of the bottle to confirm it is recyclable."),
    "can": ("Recyclable", "Blue / Recycling Collection",
            "Rinse and place in the recycling collection.",
            "Aluminum cans are highly recyclable and valuable for recovery."),
    "magazine": ("Recyclable", "Blue / Recycling Collection",
                 "Place in the recycling collection.",
                 "Glossy paper is usually still recyclable."),

    "phone": ("E-waste", "Designated E-waste Collection",
              "Take to the campus e-waste collection point; do not place in regular bins.",
              "Remove personal data and batteries where possible before disposal."),
    "mobile phone": ("E-waste", "Designated E-waste Collection",
                     "Take to the campus e-waste collection point; do not place in regular bins.",
                     "Old phones often contain recoverable metals; never bin them with general waste."),
    "charger": ("E-waste", "Designated E-waste Collection",
                "Take to the campus e-waste collection point.",
                "Cables and chargers should never go in general or organic waste."),
    "keyboard": ("E-waste", "Designated E-waste Collection",
                 "Take to the campus e-waste collection point.",
                 "Electronic peripherals often contain reusable components."),
    "laptop": ("E-waste", "Designated E-waste Collection",
               "Take to the campus e-waste collection point.",
               "Back up and wipe data before recycling a laptop."),
    "headphones": ("E-waste", "Designated E-waste Collection",
                   "Take to the campus e-waste collection point.",
                   "Small electronics should never be placed in general waste."),

    "battery": ("Hazardous", "Designated Hazardous-waste Channel",
                "Take to the designated hazardous-waste collection point; never place in regular bins.",
                "Batteries can leak harmful chemicals if disposed of incorrectly."),
    "chemicals": ("Hazardous", "Designated Hazardous-waste Channel",
                  "Take to the designated hazardous-waste collection point.",
                  "Never pour chemicals down drains or mix with other waste."),
    "paint": ("Hazardous", "Designated Hazardous-waste Channel",
              "Take to the designated hazardous-waste collection point.",
              "Let paint cans dry out fully before checking local disposal rules."),
    "medicine": ("Hazardous", "Designated Hazardous-waste Channel",
                  "Return to a pharmacy or the designated hazardous-waste channel.",
                  "Expired medicine should never be flushed or thrown in regular waste."),

    "glass bottle": ("Glass", "Glass Collection Point",
                     "Place in the glass collection point where provided.",
                     "Rinse glass containers before disposal to avoid contamination."),
    "jar": ("Glass", "Glass Collection Point",
            "Rinse and place in the glass collection point.",
            "Remove lids before recycling glass jars."),
    "broken glass": ("Glass", "Glass Collection Point",
                     "Wrap carefully before placing in the glass collection point.",
                     "Wrap broken glass to protect collection staff from injury."),

    "styrofoam": ("General", "General / Reject Waste Channel",
                  "Place in the general/reject waste channel.",
                  "Reduce use of styrofoam where reusable alternatives exist."),
    "wrapper": ("General", "General / Reject Waste Channel",
                "Place in the general/reject waste channel.",
                "Multi-layer wrappers are usually not recyclable."),
    "tissue": ("General", "General / Reject Waste Channel",
               "Place in the general/reject waste channel.",
               "Used tissues cannot be recycled or composted in most systems."),
    "diaper": ("General", "General / Reject Waste Channel",
               "Place in the general/reject waste channel.",
               "Diapers must go in general waste, never recycling.")
}

TIPS = [
    "Always rinse containers before placing them in recycling.",
    "Batteries and electronics must never go into general or organic waste.",
    "Compost organic waste where facilities are available on campus.",
    "Flatten cardboard boxes to save space in recycling bins.",
    "Carry a reusable bottle and bag to reduce single-use waste.",
    "Separate waste at the source; it is much harder to sort later.",
    "Check local campus guidelines, as bin colors differ between institutions.",
    "Donate or repair usable electronics instead of discarding them.",
    "Avoid mixing hazardous waste (chemicals, paint, medicine) with regular trash.",
    "Reduce and reuse before recycling; recycling is the last resort."
]

# History is automatically saved in the same folder as this Python file.
HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "disposal_history.json")

def load_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except (json.JSONDecodeError, OSError):
        pass
    return []

def save_history(history):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4)
    except OSError:
        print("Warning: Could not save disposal history.")

def normalize(text):
    return " ".join(text.strip().lower().split())

def identify_waste(item):
    query = normalize(item)

    if query in WASTE_DB:
        return query, WASTE_DB[query]

    best = None
    for known_item in WASTE_DB:
        if known_item in query or query in known_item:
            if best is None or len(known_item) > len(best):
                best = known_item

    if best:
        return best, WASTE_DB[best]

    return None

def header(title):
    print("\n" + "-" * 50)
    print(title)
    print("-" * 50)

def get_item():
    while True:
        item = input("Enter waste item: ").strip()
        if item:
            return item
        print("Please enter a waste item.")

def identify_menu():
    item = get_item()
    result = identify_waste(item)

    header("WASTE IDENTIFICATION")

    if result is None:
        print("Item:", item.title())
        print("Category: Unknown")
        print("\nThis item is not in our database yet.")
        print("Please check with campus facilities staff if unsure.")
        return

    name, details = result
    category, bin_name, action, tip = details

    print("Item:", name.title())
    print("Category:", category)
    print("Recommended Bin:", bin_name)
    print("\nRecommended Action:")
    print(action)
    print("\nTip:")
    print(tip)

def categories_menu():
    header("WASTE CATEGORIES")

    categories = {}
    for item, details in WASTE_DB.items():
        category = details[0]
        categories.setdefault(category, []).append(item.title())

    for category, items in sorted(categories.items()):
        print("\n" + category + ":")
        print("Examples:", ", ".join(items[:6]))

def search_menu():
    query = normalize(get_item())

    header("SEARCH RESULTS")

    found = False
    for item, details in WASTE_DB.items():
        if query in item or item in query:
            print("-", item.title(), "->", details[0])
            found = True

    if not found:
        print("No matching items found.")

def record_menu():
    item = get_item()
    result = identify_waste(item)

    if result is None:
        print("\nItem not recognized.")
        confirm = input("Record it as General waste? (y/n): ").strip().lower()
        if confirm != "y":
            print("Disposal not recorded.")
            return
        category = "General"
        display_name = item.title()
    else:
        name, details = result
        category = details[0]
        display_name = name.title()

    history = load_history()

    record = {
        "date": datetime.now().strftime("%d-%m-%Y"),
        "item": display_name,
        "category": category
    }

    history.append(record)
    save_history(history)

    header("DISPOSAL RECORDED")
    print("Date:", record["date"])
    print("Item:", record["item"])
    print("Category:", record["category"])

def statistics_menu():
    history = load_history()

    header("DISPOSAL STATISTICS")

    print("Total Items Recorded:", len(history))

    if not history:
        print("No disposal records found yet.")
        return

    counts = {}
    for record in history:
        category = record.get("category", "Unknown")
        counts[category] = counts.get(category, 0) + 1

    for category, count in sorted(counts.items()):
        print(f"{category:<15}: {count}")

    most_common = max(counts, key=counts.get)
    print("\nMost Common Category:", most_common)

def tips_menu():
    header("ENVIRONMENTAL TIPS")

    for i, tip in enumerate(TIPS, 1):
        print(f"{i}. {tip}")

def history_menu():
    history = load_history()

    header("DISPOSAL HISTORY")

    if not history:
        print("No disposal records yet.")
        return

    print(f"{'Date':<12}{'Item':<20}{'Category':<15}")
    print("-" * 50)

    for record in history:
        print(f"{record['date']:<12}{record['item']:<20}{record['category']:<15}")

def main():
    print("\nWelcome to the Campus Waste Segregation Assistant!")

    while True:
        print("""
==================================================
        CAMPUS WASTE ASSISTANT
==================================================
1. Identify Waste
2. View Waste Categories
3. Search Waste Item
4. Record Waste Disposal
5. View Disposal Statistics
6. View Environmental Tips
7. View Disposal History
8. Exit
==================================================
""")

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            identify_menu()
        elif choice == "2":
            categories_menu()
        elif choice == "3":
            search_menu()
        elif choice == "4":
            record_menu()
        elif choice == "5":
            statistics_menu()
        elif choice == "6":
            tips_menu()
        elif choice == "7":
            history_menu()
        elif choice == "8":
            print("\nThank you for using the Campus Waste Segregation Assistant!")
            print("Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a number from 1 to 8.")

if __name__ == "__main__":
    main()
