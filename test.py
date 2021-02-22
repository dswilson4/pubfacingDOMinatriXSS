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

# domains = ['www.google.com', 'www.youtube.com', 'www.tmall.com', 'www.facebook.com', 'www.baidu.com', 'www.qq.com', 'www.sohu.com', 'world.taobao.com', 
#                 'www.360.cn', 'www.amazon.com', 'corporate.jd.com', 'www.yahoo.com', 'www.wikipedia.org', 'zoom.us', 'weibo.com', 'www.sina.com.cn', 'outlook.live.com', 
#                 'www.reddit.com', 'www.xinhuanet.com', 'www.netflix.com', 'www.microsoft.com', 'www.okezone.com', 'www.vk.com', 'www.office.com', 'www.instagram.com', 'www.csdn.net', 
#                 'www.alipay.com', 'www.microsoftonline.com', 'www.myshopify.com', 'www.yahoo.co.jp', 'panda.tv', 'www.zhanqi.tv', 'www.google.com.hk', 'bongacams.com', 'www.twitch.tv', 'www.amazon.in', 
#                 'www.naver.com', 'www.bing.com', 'www.apple.com', 'www.ebay.com', 'www.aliexpress.com', 'www.tianya.cn', 'www.amazon.co.jp', 'stackoverflow.com', 'www.adobe.com', 'twitter.com', 'www.google.co.in', 
#                 'www.livejasmin.com', 'yandex.ru', 'www.tribunnews.com']

domains = []


# open file and read the content in a list
with open('alexa50-200.txt', 'r') as filehandle:
    for line in filehandle:
        # remove linebreak which is the last character of the string
        currentPlace = line[:-1]

        # add item to the list
        domains.append(currentPlace)

# office = 22

count = 1
for target in domains:
    driver = webdriver.Chrome(desired_capabilities=dc, chrome_options = options, executable_path="F:/webDriver/bin/chromedriver_win32/chromedriver")  # Optional argument, if not specified will search path.
    httpVar = False
    if count > 150:
        break
    count += 1
    print(target)
    for i in range(5):
        if not httpVar:
            try:
                targetDomain = "https://www." + target
                executeDrive(driver, targetDomain)
            except:
                print("*NEEDS TO TRY HTTP*")
                driver.quit()
                driver = webdriver.Chrome(desired_capabilities=dc, chrome_options = options, executable_path="F:/webDriver/bin/chromedriver_win32/chromedriver")  # Optional argument, if not specified will search path.
                httpVar = True
        
        # HTTP
        else:
            try:
                targetDomain = "http://www." + target
                executeDrive(driver, targetDomain)
            except:
                print("^FAILURE, SITE NOT REACHABLE^")
                driver.quit()
                driver = webdriver.Chrome(desired_capabilities=dc, chrome_options = options, executable_path="F:/webDriver/bin/chromedriver_win32/chromedriver")  # Optional argument, if not specified will search path.
                break
    driver.quit()
print("DONE")
