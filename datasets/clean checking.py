import json
import random

with open("cleaned.json", encoding="utf-8") as f:
    data = json.load(f)

print("Total records:", len(data))
print("Sample:", data[:3])

bad = [x for x in data if not x.get("text")]
print("Empty entries:", len(bad))

texts = [x["text"].lower() for x in data]
print("Unique:", len(set(texts)))
print("Total:", len(texts))



for _ in range(5):
    print(random.choice(data)["text"])

    lengths = [len(x["text"].split()) for x in data]

print("Shortest:", min(lengths))
print("Longest:", max(lengths))
print("Average:", sum(lengths)/len(lengths))