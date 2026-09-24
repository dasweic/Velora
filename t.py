import json

with open("page.json", "r", encoding="utf-8") as file:
    data = json.load(file)

def print_texts(obj):
    if isinstance(obj, dict):
        if "text" in obj:
            print(obj["text"])

        for value in obj.values():
            print_texts(value)

    elif isinstance(obj, list):
        for item in obj:
            print_texts(item)

print_texts(data)