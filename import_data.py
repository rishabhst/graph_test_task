import csv
import sys
import time


graph_id =  sys.argv[1]
filenames =  sys.argv[2].split(',')

merged_file_name = "merged_file{}.csv".format(int(time.time()))

node_ids = []
with open(merged_file_name, mode='w') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for file in filenames:
        with open(file,'r')as f:
          data = csv.reader(f, delimiter=';')
          for row in data:
                if row[1] not in node_ids:
                    node_ids.append(row[1])
                    writer.writerow([row[1], row[0], row[2],row[3],row[4], row[4]])

print("File {} is merged".format(merged_file_name))