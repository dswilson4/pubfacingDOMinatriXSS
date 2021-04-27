import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

dc = DesiredCapabilities.CHROME
dc['goog:loggingPrefs'] = { 'browser':'ALL' }

def page_is_loading(driver):
    while True:
        x = driver.execute_script("return document.readyState")
        if x == "complete":
            return True
        else:
            yield False

def executeDrive(driver, domainName):
    try:
        driver.get(domainName)
        while not page_is_loading(driver):
            time.sleep()
        time.sleep(10)
        for entry in driver.get_log('browser'):
            try:
                print(entry)
            except:
                print("ERROR PRINTING OCCURED FOR THIS DOMAIN's ENTRY")
    except:
        print("Failed execute drive")



options = Options()
options.binary_location = "F:/newChromium/chromium/src/out/domTest/chrome.exe"
# options.add_argument = "--enable-logging=stderr --vmodule"

# TEST --------------------
rootFiles = ["file:///F:/researchDevelopment/pubfacingDOMinatriXSS/sandbox/test.html",
             "file:///F:/researchDevelopment/pubfacingDOMinatriXSS/sandbox/testStatic.html"]
DOMinoURLS = ["file:///F:/researchDevelopment/pubfacingDOMinatriXSS/sandbox/test.html",
              "file:///F:/researchDevelopment/pubfacingDOMinatriXSS/sandbox/test.html?search=%22%3E%3Csvg%20onload=alert(1)%3E",
              "file:///F:/researchDevelopment/pubfacingDOMinatriXSS/sandbox/test.html?search=<img src=1 onerror=alert(1)>",
              ]

executeDrive(driver, targetDomain)


# count = 1



# for target in domains:
#     driver = webdriver.Chrome(desired_capabilities=dc, chrome_options = options, executable_path="F:/webDriver/bin/chromedriver_win32/chromedriver")  # Optional argument, if not specified will search path.
#     httpVar = False
#     if count > 150:
#         break
#     count += 1
#     print(target)
#     for i in range(5):
#         if not httpVar:
#             try:
#                 targetDomain = "https://www." + target
#                 executeDrive(driver, targetDomain)
#             except:
#                 print("*NEEDS TO TRY HTTP*")
#                 driver.quit()
#                 driver = webdriver.Chrome(desired_capabilities=dc, chrome_options = options, executable_path="F:/webDriver/bin/chromedriver_win32/chromedriver")  # Optional argument, if not specified will search path.
#                 httpVar = True
        
#         # HTTP
#         else:
#             try:
#                 targetDomain = "http://www." + target
#                 executeDrive(driver, targetDomain)
#             except:
#                 print("^FAILURE, SITE NOT REACHABLE^")
#                 driver.quit()
#                 driver = webdriver.Chrome(desired_capabilities=dc, chrome_options = options, executable_path="F:/webDriver/bin/chromedriver_win32/chromedriver")  # Optional argument, if not specified will search path.
#                 break
#     driver.quit()
# print("DONE")
