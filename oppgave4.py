import csv

with open('supporthenvendelser.csv', newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        print(row['id'], row['category'], row['minutes'], row['is_resolved'])
