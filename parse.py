
  
  

allFiles = ["alpha1_5.txt", "alpha6_10.txt", "alpha11_15.txt", "alpha16_20.txt",
            "alpha21_25.txt", "alpha26_30.txt", "alpha31_35.txt", "alpha36_40.txt",
            "alpha41_45.txt", "alpha46_50.txt"]


averages = {}

for fileName in allFiles:

    # Using readlines() 
    file1 = open(fileName, 'r') 
    Lines = file1.readlines() 
    
    count = 0

    # { domain : [ [Time to DOMContentLoaded] , [conversion time] ] }
    test_domainMap = {}
    control_domainMap = {}

    conversionMap = {}

    for line in Lines: 
        # [11788:14032:1112/042852.933:INFO:CONSOLE(102)] "Conversion time: 6.584999999176944", source: https://www.google.com/ (102)


        if "Conversion time"in line:
            if "overheadControl" in line:
                print('here')
            test = line.split('"')

            parsed = test[1].split(": ")
            # ['Conversion time', '13.59999999840511', 'https://www.google.com/']

            domainName = parsed[2]
            conversionTime = float(parsed[1])
            
            if domainName not in conversionMap:
                conversionMap[domainName] = []
            conversionMap[domainName].append(conversionTime)

        if "DOMContentLoaded" in line:
            if "overheadControl" in line:
                print('here')
            # Creates this format:
            # ['[7164:3916:1111/225853.774:INFO:CONSOLE(141)] ', 'Time to DOMContentLoaded: 1504.4950000001336', ', source: http://127.0.0.1:8887/dominatrixssStatic.js (141)\n']
            test = line.split('"')

            # Split on ": "
            # 'Time to DOMContentLoaded: 1504.4950000001336'
            parsed = test[1].split(": ")
            domainName = parsed[2]
            timeToDOM = float(parsed[1])


            if (parsed[3] == 'overhead'):
                if domainName not in control_domainMap:
                    control_domainMap[domainName] = [[], []]
                control_domainMap[domainName][0].append(timeToDOM)
            else:
                if domainName not in test_domainMap:
                    test_domainMap[domainName] = [[], []]
                test_domainMap[domainName][0].append(timeToDOM)

    print("TEST MAP: ")
    print(test_domainMap)
    print("\n")
    print("CONTROL MAP: ")
    print(control_domainMap)
    print("\n")



    print("TEST MAP: ")
    for url in test_domainMap.keys():
        print("Time to DOMContentLoaded: " + url + " " + str(sum(test_domainMap[url][0])/len(test_domainMap[url][0])))

    print("\n")
    print("CONTROL MAP: ")
    for url in control_domainMap.keys():
        print("Time to DOMContentLoaded: " + url + " " + str(sum(control_domainMap[url][0])/len(control_domainMap[url][0])))


    print("\n")
    print("CONVERSION MAP: ")
    for url in conversionMap.keys():
        print("Conversion Time: "+ url + " " + str(sum(conversionMap[url])/len(conversionMap[url])))
    
    

    # Add to averages map

    for url in conversionMap.keys():
        averageOverhead = sum(conversionMap[url])/len(conversionMap[url]) / sum(test_domainMap[url][0])/len(test_domainMap[url][0])
        averages[url] = str(averageOverhead * 100)


    #         timedValues.append(float(savedVal))
    #         print(savedVal)
    #     # print("Line{}: {}".format(count, line.strip())) 

    # print("average: " + str(sum(timedValues)/len(timedValues)))

summedAverages = []

print("\n")
for key in averages:
    print("AVERAGE: " + averages[key] + " URL: " + key)
    summedAverages.append(float(averages[key]))
print("\n")
print(summedAverages)
print('\n')

print("TOTAL AVERAGE: " + str(sum(summedAverages)/len(summedAverages)))

