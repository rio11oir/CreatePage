# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 10:34:51 2015

@author: christopher.wong, rashad.haque
"""


# THINGS TO CHANGE:
csvName = "Pearsall Independent School District2.csv"
oldSite = "http://www.pearsallisd.org//"
startingPage = "http://pearsall.ss8.sharpschool.com/cms/One.aspx?portalId=777834&pageId=777842"
loginPage = "http://pearsall.ss8.sharpschool.com/gateway/Login.aspx?ReturnUrl=%2f"
divName = 'articleBody'
divNameBackUp = 'content2'


from bs4 import BeautifulSoup
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.webdriver import FirefoxProfile
import time
import urllib.request

#global isOldPage
#isOldPage = False

# checks through the csv file for any errors that may appear
def csvCheck():
    checkcel = open(csvName, "r")
    lineNum = 0
   
    while True:
        checkcelLine = checkcel.readline().rstrip()
        lineNum += 1
        
        if checkcelLine == "":
            break
        
        checkcelLine = checkcelLine.strip(' ,"')        
        
        pageChar = checkcelLine[0]
        if str(pageChar).isdigit() :
            checkcelLine = checkcelLine[1:]
        else:
            pageChar = '0'
        
        nameAndLink = splitLine(checkcelLine)
        
        try:
            nameAndLink[0]
        except:
            print("CSV Error at: " + str(nameAndLink) + " at " + str(lineNum))
            nameAndLink[0]
    
        # if content space page or teacher page or ext link page, requires an old site URL
        if pageChar == '0' or pageChar == '8' or pageChar == '1':
            try:
                nameAndLink[1]
            except:
                print("CSV Error at: " + str(nameAndLink) + " at " + str(lineNum))
                nameAndLink[1]
    print("Done Checking") 
    checkcel.close

# enter the title when creating a new page and press submit
def enter_title(name):
    testID = getID(driver, "ctl00_ContentPlaceHolder1_ctl00_txtTitle")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, testID)))
    
    textbox = driver.find_element_by_id(testID)
    textbox.send_keys(Keys.CONTROL + "a")    
    textbox.send_keys(name)
    
    
    #driver.find_element_by_id(getID(driver, "ctl00_ContentPlaceHolder1_ctl00_btnSubmit")).click()


# Checks for duplicate page error

def dupPageCheck(name):
    # if page with same name already exists
    n=0
    while True:
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "reMode_html")))
            break
        except:
            n += 1
            enter_title(name + ' (' + str(n) + ')')
            driver.find_element_by_id(getID(driver, "ctl00_ContentPlaceHolder1_ctl00_btnSubmit")).click()
            
    if n>0:
        print("Duplicate Page: " + name + ' (' + str(n) + ')')
        

"""
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "reMode_html")))
    
    if EC.text_to_be_present_in_element(EC.visibility_of_element_located('ctl00_ContentPlaceHolder1_ctl06_lblError'), 'Error!   The page name already exists..'):
        print('found')
        navLinkList = driver.find_elements_by_class_name("navLink")
        
        for x in range(0,len(navLinkList)-1):
            navLinkList[x].click()
            #request = urllib.request.Request(url)

            if driver.title.find(name) == 0:
                break
            driver.back()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "navLink")))
            navLinkList = driver.find_elements_by_class_name("navLink")
            
        global isOldPage
        isOldPage = True
        
        # click Edit
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_ctl00_ctl00_menu_m0").click()
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_ctl00_ctl00_menu_m0_m0").click()
"""


# Creates an external link page
# pageType = [0,1,2]: 0 - ext link, 1 - file, 2 - internal page
def ext_page(nameAndLink):
    name = nameAndLink[0]
    link = nameAndLink[1]
    # first character of the link will describe what type of link it is
    # 0 - external link
    # 1 - internal file
    # 2 - internal page
    pageType = link[0]
    link = link[1:]
    
    enter_title(name)
   
    # enter the page name
    #testID = getID(driver, "ctl00_ContentPlaceHolder1_ctl00_txtTitle")
    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, testID)))
    #driver.find_element_by_id(testID).send_keys(name)
    
    driver.find_element_by_id(getID(driver, "ctl00_ContentPlaceHolder1_ctl00_hplGetName")).click()
   
    if pageType == '0':
        # enter the web address
        driver.find_element_by_id(getID(driver, "ctl00_ContentPlaceHolder1_ctl00_txtUrl")).send_keys(link)
        if 'https://' in link:
            select = Select(driver.find_element_by_id(getID(driver, "ctl00_ContentPlaceHolder1_ctl00_ddlProtocol")))
            select.select_by_visible_text('https://')
    elif pageType == '1':
        # click the 'Browse in File System' button
        driver.find_element_by_id(getID(driver, "ctl00_ContentPlaceHolder1_ctl00_rblTypes_1")).click()
        # enter the web address
        driver.find_element_by_id(getID(driver, "ctl00_ContentPlaceHolder1_ctl00_txtUrl")).send_keys(link)
        driver.find_element_by_id(getID(driver, "chkBtn")).click()
        WebDriverWait(driver, 10000).until(EC.text_to_be_present_in_element_value((By.ID, 'statusBox'), 'Done'))
        EC.text_to_be_present_in_element_value
    elif pageType == '2':
        # click the 'Browse Internal Pages' button
        driver.find_element_by_id(getID(driver, "ctl00_ContentPlaceHolder1_ctl00_rblTypes_2")).click()
        # click 'Browse'
        driver.find_element_by_id(getID(driver, "ctl00_ContentPlaceHolder1_ctl00_btnBrowse")).click()
        # switch to the new pop up window
        driver.switch_to_window(driver.window_handles[-1])
        # switch to the frame inside the window
        driver.switch_to.frame("browser")
        # search for the page name and choose the first result which shows up
        driver.find_element_by_id(getID(driver, "ctl00_ContentPlaceHolder1_ctl00_txtSearchField")).send_keys(name)
        driver.find_element_by_id(getID(driver, "ctl00_ContentPlaceHolder1_ctl00_btnSearch")).click()
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_ctl00_gvGridView_ctl02_hplInsert").click()
        # switch back to the original Add Link window
        driver.switch_to_window(driver.window_handles[-1])
    else:
        if link == "":
            driver.find_element_by_id(getID(driver, "ctl00_ContentPlaceHolder1_ctl00_txtUrl")).send_keys("blank space link place holder")
        else:
            driver.find_element_by_id(getID(driver, "ctl00_ContentPlaceHolder1_ctl00_txtUrl")).send_keys(link)
       
    # create page
    driver.find_element_by_id(getID(driver, "ctl00_ContentPlaceHolder1_ctl00_btnSubmit")).click()

# Creates a content page
def content_page(nameAndLink):
    name = nameAndLink[0]
    url = nameAndLink[1]
    #global isOldPage
    #if isOldPage:
        
    # copy content from old site
    if not (url==None or url.lower()=="new page"):
        request = urllib.request.Request(url)
        result = urllib.request.urlopen(request)
        html = result.read()
        soup = BeautifulSoup(html, "lxml")
        content = soup.select('div#' + divName)
        if (str(content) == None or str(content) == ''):
            content = soup.find('div', id_ = divName)
            if (str(content) == None or str(content) == ''):
                content = soup.find('div', id_ = divNameBackUp)
        
        content.append("")
        content = str(content[0])
        
        """
        if content.find('src="/') ==-1 or content.find('src="' + oldSite)==-1 :
            content = content.replace('src="', 'src="' + oldSite)
        else:    
            content = content.replace('src="/', 'src="' + oldSite)
        """
        content = content.replace('src="/', 'src="' + oldSite)
        content = content.replace('href="/', 'href="' + oldSite)
        
        # In case page with same name exists
        dupPageCheck(name)
        
        # paste the code into the HTML editor
        driver.find_element_by_class_name("reMode_html").click()
        textbox = driver.find_elements_by_tag_name("iframe")[1]
        time.sleep(1)
        pyperclip.copy(content)
        textbox.send_keys(Keys.CONTROL + "a")
        textbox.send_keys(Keys.CONTROL + "v")
        
        # Extension things
        driver.find_element_by_id(getID(driver, "loadBtn")).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, getID(driver, "stripBtn"))))
        driver.find_element_by_id(getID(driver, "stripBtn")).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, getID(driver, "startBtn"))))
        driver.find_element_by_id(getID(driver, "startBtn")).click()
        WebDriverWait(driver, 1000000).until(EC.element_to_be_clickable((By.ID, getID(driver, "startBtn"))))
    
    # publish the page
    driver.find_element_by_id(getID(driver, "ctl00_ContentPlaceHolder1_ctl00_ibPublishBottom")).click()
    #if not isOldPage:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, getID(driver, "ctl00_ContentPlaceHolder1_ctl00_btnYes"))))
    driver.find_element_by_id(getID(driver, "ctl00_ContentPlaceHolder1_ctl00_btnYes")).click()

    
# Get the correct ID for buttons/links
def getID(driver, baseID):
        
    for ID in range (0, 10): 
        try:
            testID = baseID.replace("ContentPlaceHolder1_ctl00", "ContentPlaceHolder1_ctl0" + str(ID))
            if (ID == 0):
                WebDriverWait(driver, 0.5).until(EC.visibility_of_element_located((By.ID, testID)))
            
            element = driver.find_element_by_id(testID)
            if element.is_displayed():
                break
        except:
            continue

    testID = "".join(testID)
    return testID
    
    
# Separate page name and old site URL 
    #nameAndLink[0] is the name, nameAndLink[1] is the link
def splitLine(excelLine):
    nameAndLink = excelLine.rsplit(',', 1)
    
    nameAndLink[0] = nameAndLink[0].strip(' ,"')
    nameAndLink[0] = nameAndLink[0].replace("\"\"","\"")
    
    if len(nameAndLink) >1:
        nameAndLink[1] = nameAndLink[1].strip(' ,"')
    
    return nameAndLink

    
# Checking for errors that can cause breaks in the csv
csvCheck()

# initial setup: start Firefox and login to website
firefoxProfile = FirefoxProfile("..\FF Profile")
driver = webdriver.Firefox(firefox_profile=firefoxProfile)
driver.get(loginPage)
driver.find_element_by_name("ctl00$ContentPlaceHolder1$txtUsername").send_keys(input("Username: "))
driver.find_element_by_name("ctl00$ContentPlaceHolder1$txtPassword").send_keys(input("Password: "))
driver.find_element_by_name("ctl00$ContentPlaceHolder1$btnLogin").click()

excelLine = "-1"
commaCount = 0
currCommaCount = -1
pagePath = []

#currPage = input("Please enter the URL of the SharpSchool site which you would like to create the pages on: ")
currPage = startingPage
pagePath.append(currPage)

# Open the .csv file which contains the website skeleton
# excelSheet = open(input("Please enter the file name: "), "r")
#excelSheet = open("Laingsburg Community Schools.csv", "r")
excelSheet = open(csvName, "r")
#divName = input("Please enter the class or ID name of the div which contains the content on the old site: ")

print("Migration beginning...")
# Creates all pages on the .csv file
while True:
    # variable reset
    #global isOldPage
    #isOldPage = False    
    
    # read in the next line from the Excel sheet
    excelLine = excelSheet.readline().rstrip()
    
    # Check if the file is done (first blank line)
    if excelLine == "":
        break
    
    i = 0
    commaCount = 0 
    
    while (excelLine[i] == ','):
        i+= 1
        commaCount+= 1
            
    excelLine = excelLine.lstrip(',')
    
    # Checks level of the new page (wrt to current)    
    if commaCount == currCommaCount:
        # driver.back()
        pagePath.pop()
        currPage = pagePath.pop()
    elif commaCount < currCommaCount:
        # Crazy back tracking code
        for x in range(commaCount, currCommaCount+1):
            pagePath.pop()
        currPage = pagePath.pop()
    else:
        currPage = pagePath.pop()
    
    pagePath.append(currPage)
    currCommaCount = commaCount
    
    excelLine = excelLine.strip(' ,"')
    # Check for type of page we want:
    # 0 - Content Space
    # 1 - External Link
    # 2 - Photo Gallery
    # 3 - Document Container
    # 4 - Calendar
    # 5 - Form Page
    # 6 - Discussion - currently not supported
    # 7 - News
    # 8 - Teacher Page
    # 9 - Blog - currently not supported
    # A/9 - Wiki
    pageChar = excelLine[0]
    if str(pageChar).isdigit() :
        excelLine = excelLine[1:]
        
    if pageChar == '0':
        addOn = "&action=addTypedPage&parentId=######&pageType=Content+Space+Page"
    elif pageChar == '1':
        addOn = "&action=addextlinkpage&parentId=######"
    elif pageChar == '2':
        addOn = "&action=addTypedPage&parentId=######&pageType=Photo+Gallery+Page"
    elif pageChar == '3':
        addOn = "&action=addTypedPage&parentId=######&pageType=Document+Container+Page"
    elif pageChar == '4':
        addOn = "&action=addTypedPage&parentId=######&pageType=Calendar+Page"
    elif pageChar == '5':
        addOn = "&action=addTypedPage&parentId=######&pageType=Form+Page"
    #elif pageChar == '6':
    #    addOn = "&action=addTypedPage&parentId=#######&pageType=Discussion+Forum+page"
    elif pageChar == '7':
        addOn = "&action=addTypedPage&parentId=######&pageType=News+Section+Page"
    elif pageChar == '8':
        addOn = "&action=addTypedPage&parentId=######&pageType=Teacher+Page"
    #elif pageChar == '9':
    #    addOn = "&action=addblogpage&parentId=######"
    elif pageChar == '9':
        addOn = "&action=addTypedPage&parentId=######&pageType=Wiki+Page"
    else:
        addOn = "&action=addTypedPage&parentId=######&pageType=Content+Space+Page"
        pageChar = '0'
        
    # find current page (parent) ID
    pageId = currPage[(currPage.rfind("pageId=") + 7):]
    
    while not pageId.isdigit():
        pageId = pageId[:-1]
        
    if currPage.find("&action=") > -1:
        currPage = currPage[:currPage.find("&action=")]
    
    addOn = addOn.replace("######",pageId)
    
    #currPage = currPage + addOn
    driver.get(currPage + addOn)
    
    # Create external page
    if pageChar == '1':
        ext_page(splitLine(excelLine))
    # Create all other types of pages
    else:
        # Separate page name and old site URL
        nameAndLink = splitLine(excelLine)
        enter_title(nameAndLink[0])
        driver.find_element_by_id(getID(driver, "ctl00_ContentPlaceHolder1_ctl00_btnSubmit")).click()

        
    # if ext link page or blog page, it ends up on the parent page
    if pageChar == '1' or pageChar == '9': 
        pagePath.pop()
        currCommaCount = currCommaCount - 1    
    # if content space page or teacher page, there is a 2nd step (and requires an old site URL)
    elif pageChar == '0' or pageChar == '8':
        #dupPageCheck(nameAndLink[0])
        content_page(nameAndLink)

        
    pagePath.append(driver.current_url)

excelSheet.close()
print("Migration complete! :D")