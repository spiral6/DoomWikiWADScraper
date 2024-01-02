import json

with open('result.json', 'r', encoding="utf-8") as file:
    PWADS = json.load(file)

count = 0

for PWAD in PWADS:
    PWAD["filename"] = ""
    PWAD["ID"] = count
    count = count + 1

with open('result.json', 'w', encoding="utf-8") as file:
    json.dump(PWADS, file, ensure_ascii=False)