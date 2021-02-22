import json

import ast

from collections import defaultdict
domains = []


# open file and read the content in a list
with open('alexa50-200.txt', 'r') as filehandle:
    for line in filehandle:
        # remove linebreak which is the last character of the string
        currentPlace = line[:-1]

        # add item to the list
        domains.append(currentPlace)

  
  

allFiles = ["DOMinoRun.txt", "plusPlusRun.txt", "controlRun.txt"]

plusplus_domainMap = {}

control_domainMap = {}

for fileName in allFiles:

    if "DOMino" in fileName:
        continue 

    # Using readlines() 
    file1 = open(fileName, 'r') 
    Lines = file1.readlines() 
    
    count = 0

    # { domain : [ [Time to DOMContentLoaded] , [conversion time] ] }
    test_domainMap = {}


    for line in Lines: 
        # [11788:14032:1112/042852.933:INFO:CONSOLE(102)] "Conversion time: 6.584999999176944", source: https://www.google.com/ (102)

        unreachableDomainErrors = ["ERROR PRINTING OCCURED FOR THIS DOMAIN", "*NEEDS TO TRY HTTP*", "^FAILURE, SITE NOT REACHABLE^"]
        if line.strip() in domains:
            continue
        if line.strip() in unreachableDomainErrors:
            continue
        trimmed = line.strip()
        try:
            jsonObj = ast.literal_eval(trimmed)
        except:
            print("FAILED HERE")
            print(trimmed)
            continue

        # print(jsonObj)
        if "Conversion time" in jsonObj['message']:
            # print('here')
            forDomain = jsonObj['message'].split(' ')
            # print(forDomain[0])
            domainName = forDomain[0]
            # print(jsonObj['message'])

            forValue = jsonObj['message'].split(': ')
            print("forVal")
            measuredMs = float(forValue[1])
            print(measuredMs)

            if domainName not in test_domainMap:
                test_domainMap[domainName] = ([], [])
            else:
                test_domainMap[domainName][1].append(measuredMs)

            # print(count)
        if "Time to DOMContentLoaded" in jsonObj['message']:
            # print('here')
            forDomain = jsonObj['message'].split(' ')
            # print(forDomain[0])
            domainName = forDomain[0]
            # print(jsonObj['message'])

            forValue = jsonObj['message'].split(': ')
            measuredMs = float(forValue[1])
            # print(measuredMs)

            if domainName not in test_domainMap:
                test_domainMap[domainName] = ([], [])
            else:
                test_domainMap[domainName][0].append(measuredMs)
            # print(count)

        
        count += 1

    

    print("TEST MAP: ")
    print(test_domainMap)
    print("\n")



    print("TEST MAP: ")
    for url in test_domainMap.keys():
        print("\n")
        print(url)
        if len(test_domainMap[url][0]) > 0:
            print("Time to DOMContentLoaded: " + url + " " + str(sum(test_domainMap[url][0])/len(test_domainMap[url][0])))
        if len(test_domainMap[url][1]) > 0:
            print("Conversion time: " + url + " " + str(sum(test_domainMap[url][1])/len(test_domainMap[url][1])))

    
    if "control" in fileName:
        for url in test_domainMap.keys():
            # if url not in domains:
            #     continue
            control_domainMap[url] = test_domainMap[url]
    else:
        for url in test_domainMap.keys():
            # if url not in domains:
            #     continue
            plusplus_domainMap[url] = test_domainMap[url]

# print(control_domainMap)

controlAverage = 0
for url in control_domainMap.keys():
    if len(control_domainMap[url][0]) > 0:
        avg = sum(control_domainMap[url][0]) / len(control_domainMap[url][0])
        controlAverage += avg
        print(url + ": " + str(avg))
controlAverage = controlAverage / len(control_domainMap.keys())

print("-----------------------")

testAverage = 0
eventConversion = 0
convertedCount = 0
for url in plusplus_domainMap.keys():
    if len(plusplus_domainMap[url][0]) > 0:
        avg = sum(plusplus_domainMap[url][0]) / len(plusplus_domainMap[url][0])

        print(url + ": " + str(avg))
        if (len(plusplus_domainMap[url][1]) == 0):
            continue
        convertedCount += 1
        conversionAvg = sum(plusplus_domainMap[url][1]) / len(plusplus_domainMap[url][1])
        eventConversion += conversionAvg
        ratio = conversionAvg / avg
        testAverage += ratio

eventConversion = eventConversion / convertedCount
testAverage = testAverage / convertedCount

print("-----------------------")
print("CONVERSION TIME")
print("-----------------------")
for url in plusplus_domainMap.keys():
    if len(plusplus_domainMap[url][1]) > 0:
        avg = sum(plusplus_domainMap[url][1]) / len(plusplus_domainMap[url][1])
        print(url + ": " + str(avg))

print("-----------------------")
print("PERCENTS")
print("-----------------------")
# print(plusplus_domainMap)

percMap = {}

for url in control_domainMap.keys():
    try:
        keyCheck = len(control_domainMap[url][0]) > 0 and len(plusplus_domainMap[url][0]) > 0
    except:
        continue
    if len(control_domainMap[url][0]) > 0 and len(plusplus_domainMap[url][0]) > 0:
        converted = sum(control_domainMap[url][0]) / len(control_domainMap[url][0])
        timeToDOMContentLoaded = sum(plusplus_domainMap[url][0]) / len(plusplus_domainMap[url][0])

        percent = converted / timeToDOMContentLoaded
        print(url + ": " + str(percent))
        percMap[url] = percent

# Overhead measurements
finalAvg = sum(percMap.values()) / len(percMap.values())
print("FINAL AVG: " + str(finalAvg))


print(controlAverage)
print(conversionAvg)
print(testAverage)