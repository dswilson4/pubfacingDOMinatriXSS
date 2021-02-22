# importing csv module 
import csv 
  
# csv file name 
filename = "ALEXA TOP 200 - Sheet1.csv"
  
# initializing the titles and rows list 
fields = [] 
rows = [] 
  
# reading csv file 
with open(filename, 'r') as csvfile: 
    # creating a csv reader object 
    csvreader = csv.reader(csvfile) 
      
    # extracting field names through first row 
    fields = next(csvreader) 
  
    # extracting each data row one by one 
    for row in csvreader: 
        rows.append(row) 
  
    # get total number of rows 
    print("Total no. of rows: %d"%(csvreader.line_num)) 
  
# printing the field names 
print('Field names are:' + ', '.join(field for field in fields)) 

domains = []

#  printing first 5 rows 
print('\nFirst 5 rows are:\n') 
count = 0 
for row in rows: 
    if count == 150:
        break
    # parsing each column of a row 
    if count % 6 == 0:
        print("COUNT IS : " + str(count))
        for col in row:
            domains.append(col)
            print("%10s"%col), 
            print("------")
        print('\n')
        count += 1
        continue
    print('\n') 
    count += 1
    continue
print(domains)


with open('alexa50-200.txt', 'w') as filehandle:
    for listitem in domains:
        filehandle.write('%s\n' % listitem)