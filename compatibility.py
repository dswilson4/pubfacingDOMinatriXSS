
# ----------------------------------------------

# ------------Compatability Study---------------

# ----------------------------------------------


# {URL: # of CSP violations (broken scripts)}

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



domino_violationMap = defaultdict(int)
plusPlus_violationMap = defaultdict(int)

count = 0
forDomino = 0
forPlusPlus = 0
# allFiles = ["DOMinoRun.txt", "plusPlusRun.txt"]
nonceFinder = defaultdict(int)
allFiles = ["secondControl.txt", "secondDisableDynamic.txt"]
for fileName in allFiles:

    if "plusPlus" in fileName:
        forPlusPlus += 1
    if "DOMinoRun" in fileName:
        forDomino += 1

    # Using readlines() 
    file1 = open(fileName, 'r') 
    Lines = file1.readlines() 
    
    # count = 0



    for line in Lines: 
        # [11788:14032:1112/042852.933:INFO:CONSOLE(102)] "Conversion time: 6.584999999176944", source: https://www.google.com/ (102)

        unreachableDomainErrors = ["ERROR PRINTING OCCURED FOR THIS DOMAIN", "*NEEDS TO TRY HTTP*", "^FAILURE, SITE NOT REACHABLE^"]
        if line.strip() in domains:
            # This is printing the current domain of interest
            # print(line)
            continue
        if line.strip() in unreachableDomainErrors:
            continue
        trimmed = line.strip()
        try:
            jsonObj = ast.literal_eval(trimmed)
        except:
            continue

        # print(jsonObj)
        if "nonce" in jsonObj['message']:
            nonceFinder[fileName] += 1
            # print('here')
            forDomain = jsonObj['message'].split(' ')
            # print(forDomain[0])
            domainName = forDomain[0].lower()
            # print(jsonObj['message'])

            # Search to determine if domain belongs to domain found in webpage
            belongs = False
            for element in domains:
                websiteName = element
                if ".com" in element:
                    # websiteName = splitWebsiteName[0].lower()
                    websiteName = websiteName.lower()
                if websiteName in domainName:
                    belongs = True
                    break
            if count < 5:
                print(belongs)
                print(domainName)
                count += 1
            if belongs:
                if "DisableDynamic" in fileName:
                    plusPlus_violationMap[domainName] += 1

                else:
                    domino_violationMap[domainName] += 1

print("-----------------------")
print("DOMINO")
print("-----------------------")
print(domino_violationMap)

print(sum(domino_violationMap.values()))
print(forDomino)
print("\n")
print("-----------------------")
print("PLUSPLUS")
print("-----------------------")
print(sum(plusPlus_violationMap.values()))
print(plusPlus_violationMap)

print(forPlusPlus)


print(len(domino_violationMap.keys()))
print(len(plusPlus_violationMap.keys()))
domino_domainMap = defaultdict(int)
plusplus_domainMap = defaultdict(int)
print(nonceFinder)

# Adjusting for five refreshes --------------

adjustedDominoMap = defaultdict(float)
adjustedpluPlusMap = defaultdict(float)
for element in domino_violationMap.keys():
    adjustedVal = domino_violationMap[element] * 0.2
    adjustedDominoMap[element] += adjustedVal
for element in plusPlus_violationMap.keys():
    adjustedVal = plusPlus_violationMap[element] * 0.2
    adjustedpluPlusMap[element] += adjustedVal

print(adjustedDominoMap)

# Adjusting for five refreshes --------------


# Keys for pdf default dictionaries are number of script errors, freqency is the value
pdfDomino = {}
pdfPlusPlus = {}

pdfDomino[1] = 0
pdfPlusPlus[1] = 0

for element in adjustedDominoMap.keys():
    if adjustedDominoMap[element] <= 1:
        pdfDomino[1] += 1
    else:
        formattedInt = round(adjustedDominoMap[element])
        if formattedInt not in pdfDomino.keys():
            pdfDomino[formattedInt] = 0
        pdfDomino[formattedInt] += 1

for element in adjustedpluPlusMap.keys():
    if adjustedpluPlusMap[element] <= 1:
        pdfPlusPlus[1] += 1
    else:
        formattedInt = round(adjustedpluPlusMap[element])
        if formattedInt not in pdfPlusPlus.keys():
            pdfPlusPlus[formattedInt] = 0
        pdfPlusPlus[formattedInt] += 1
# 200 is total number of tested websites



pdfDomino[0] = 200 - len(adjustedDominoMap.keys())
pdfPlusPlus[0] = 200 - len(adjustedpluPlusMap.keys())


# Be sure all keys have a value
scriptErrorNumber = 100 + 1

for i in range(scriptErrorNumber):
    if i not in pdfDomino.keys():
        pdfDomino[i] = 0
    if i not in pdfPlusPlus.keys():
        pdfPlusPlus[i] = 0



numberOfDomains = []
for i in range(scriptErrorNumber):
    numberOfDomains.append(i)


dominoIncompatible = [0]
plusIncompatible = [0]
for i in range(scriptErrorNumber):
    lastDomino = dominoIncompatible[len(dominoIncompatible) - 1]
    dominoIncompatible.append(lastDomino + pdfDomino[i]*1/200)

    lastPlus = plusIncompatible[len(plusIncompatible) - 1]
    plusIncompatible.append(lastPlus + pdfPlusPlus[i]*1/200)


import matplotlib
import matplotlib.pyplot as plt

# Data for plotting
t = []
for i in range(scriptErrorNumber):
    t.append(i)

# Ignore value of 0 to begin with
dominoGraph = dominoIncompatible[1:]
plusGraph = plusIncompatible[1:]

plt.plot(t, dominoGraph, label = "DOMino")
plt.plot(t, plusGraph, label = "DOMino++")
plt.xlabel("Number of incompatible scripts (0 -" + str(scriptErrorNumber - 1) + ")")
plt.ylabel("Density of websites (%)")
plt.title("CDF of script compatibility for DOMino and DOMino++ over Alexa top 200 domains")
plt.legend()
plt.show()

# def checkURL(domainList, fullURL):
#     for element in domainList:
#         if element.lower() in fullURL:
#             return True, element
#     return False, ""

# dominoTotalDomains = 0
# dominoScriptMap = {}
# for element in domino_violationMap:
#     dominoTotalDomains += 1
#     shouldAdd, urlToAdd = checkURL(domains, element)
#     domino_domainMap[urlToAdd] += domino_violationMap[element]
#     if domino_violationMap[element] not in dominoScriptMap.keys():
#         dominoScriptMap[domino_violationMap[element]] = 0
#     dominoScriptMap[domino_violationMap[element]] += 1

# plusTotalDomains = 0
# plusScriptMap = {}
# for element in plusPlus_violationMap:
#     plusTotalDomains += 1
#     shouldAdd, urlToAdd = checkURL(domains, element)
#     plusplus_domainMap[urlToAdd] += plusPlus_violationMap[element]
#     if plusPlus_violationMap[element] not in plusScriptMap.keys():
#         plusScriptMap[plusPlus_violationMap[element]] = 0
#     plusScriptMap[plusPlus_violationMap[element]] += 1

# print(domino_domainMap)
# print(len(domino_domainMap.keys()))
# print("\n")
# print("total Domino domains: " + str(dominoTotalDomains))

# # for element in domino_domainMap
# print(plusplus_domainMap)
# print(len(plusplus_domainMap.keys()))
# print("total Plus domains: " + str(plusTotalDomains))

# dominoScriptMap[0] = 0
# dominoScriptMap[0] += 150 - len(domino_domainMap.keys())
# curr = 150 - len(domino_domainMap.keys())
# sortedKeys = list(domino_domainMap.keys())
# sortedKeys.sort()
# print(sortedKeys)
# print(dominoScriptMap)
# # while curr < 150:


# plusScriptMap[0] = 0
# plusScriptMap[0] += 150 - len(plusScriptMap.keys())
# print(plusScriptMap)


##############################################################################

# import matplotlib
# import matplotlib.pyplot as plt

# # Data for plotting
# t = []
# for i in range(150):
#     t.append(i + 1)
# s = 1 + np.sin(2 * np.pi * t)

# fig, ax = plt.subplots()
# ax.plot(t, s)

# ax.set(xlabel='time (s)', ylabel='voltage (mV)',
#        title='About as simple as it gets, folks')
# ax.grid()

# fig.savefig("test.png")
# plt.show()

# dominoKeys = len(domino_violationMap.keys())


    # print("\n")
    # print("CONTROL MAP: ")
    # for url in control_domainMap.keys():
    #     print("Time to DOMContentLoaded: " + url + " " + str(sum(control_domainMap[url][0])/len(control_domainMap[url][0])))


    # print("\n")
    # print("CONVERSION MAP: ")
    # for url in conversionMap.keys():
    #     print("Conversion Time: "+ url + " " + str(sum(conversionMap[url])/len(conversionMap[url])))
    
    

    # # Add to averages map

    # for url in conversionMap.keys():
    #     averageOverhead = sum(conversionMap[url])/len(conversionMap[url]) / sum(test_domainMap[url][0])/len(test_domainMap[url][0])
    #     averages[url] = str(averageOverhead * 100)


    #         timedValues.append(float(savedVal))
    #         print(savedVal)
    #     # print("Line{}: {}".format(count, line.strip())) 

    # print("average: " + str(sum(timedValues)/len(timedValues)))

# summedAverages = []

# print("\n")
# for key in averages:
#     print("AVERAGE: " + averages[key] + " URL: " + key)
#     summedAverages.append(float(averages[key]))
# print("\n")
# print(summedAverages)
# print('\n')

# print("TOTAL AVERAGE: " + str(sum(summedAverages)/len(summedAverages)))

