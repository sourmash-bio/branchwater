import csv
import sys

with open(sys.argv[1], "r") as f:
    datasets = csv.DictReader(f, delimiter=",")
    print(",Run,ScientificName")
    for i, row in enumerate(datasets):
        run = row["Run"]
        sn = row["ScientificName"]
        print(f"{i},{run},{sn}") 
