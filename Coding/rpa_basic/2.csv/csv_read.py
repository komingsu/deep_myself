import csv

f = open("coffeeshop_data.csv", "r", encoding="utf-8")
rd = csv.reader(f)

for i in rd:
    print(type(i))