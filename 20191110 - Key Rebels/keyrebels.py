import csv

# print("hi")

with open('dataset.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    # print spamreader
    linecount = 0
    for row in spamreader:
        if(linecount == 0):
            # print('Column names are' + repr({", ".join(row)}))
            print('Column names are : ' + ', '.join(row))
            linecount+=1
        else:
            print ', '.join(row)