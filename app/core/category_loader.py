import csv

def load_categories(path: str):
    categories = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            categories.append(row)
    return categories