# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 10:34:51 2015

@author: christopher.wong, rashad.haque
"""

from bs4 import BeautifulSoup
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import urllib.request

isOldPage = False

# enter the title when creating a new page and press submit
def enter_title(name):
    testID = getID(driver, "ctl00_ContentPlaceHolder1_ctl00_txtTitle")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, testID)))
    driver.find_element_by_id(testID).send_keys(name)
    driver.find_element_by_id(getID(driver, "ctl00_ContentPlaceHolder1_ctl00_btnSubmit")).click()
    #if EC.visibility_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_ctl05_lblError")):
    #    driver.find_element_by_title(name).click()
    #    global isOldPage
    #    isOldPage = True
     
# Creates an external link page
# pageType = [0,1,2]: 0 - ext link, 1 - file, 2 - internal page
def ext_page(excelLine):
    # get the page name and link from the line read in from the Excel sheet    
    name, link = excelLine.rsplit(',', 1)
    name = name.strip(' ,"')
    link = link.strip(' ,"')
    name = name.replace("\"\"","\"")
   
    # first character of the link will describe what type of link it is
    # 0 - external link
    # 1 - internal file
    # 2 - internal page
    pageType = link[0]
    link = link[1:]
   
    # enter the page name
    testID = getID(driver, "ctl00_ContentPlaceHolder1_ctl00_txtTitle")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, testID)))
    driver.find_element_by_id(testID).send_keys(name)
    driver.find_element_by_id(getID(driver, "ctl00_ContentPlaceHolder1_ctl00_hplGetName")).click()
   
    if pageType == '0':
        # enter the web address
        driver.find_element_by_id(getID(driver, "ctl00_ContentPlaceHolder1_ctl00_txtUrl")).send_keys(link)
    elif pageType == '1':
        # click the 'Browse in File System' button
        driver.find_element_by_id(getID(driver, "ctl00_ContentPlaceHolder1_ctl00_rblTypes_1")).click()
        # enter the web address
        driver.find_element_by_id(getID(driver, "ctl00_ContentPlaceHolder1_ctl00_txtUrl")).send_keys(link)
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
        driver.find_element_by_id(getID(driver, "ctl00_ContentPlaceHolder1_ctl00_gvGridView_ctl02_hplInsert")).click()
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
def content_page(url):
    global isOldPage
    if isOldPage:
        # click Edit
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_ctl00_ctl00_menu_m0_m0").click()
    # copy content from old site
    if not (url==None or url.lower()=="new page"):
        request = urllib.request.Request(url)
        result = urllib.request.urlopen(request)
        html = result.read()
        soup = BeautifulSoup(html, "lxml")
        content = soup.find("div", class_ = divName)
        if (str(content) == None):
            content = soup.find("div", id_ = divName)
        # paste the code into the HTML editor
        html_window = driver.find_element_by_class_name("reMode_html")
        html_window.send_keys(Keys.RETURN)    
        textbox = driver.find_elements_by_tag_name("iframe")[1]
        time.sleep(1)
        content = str(content)
        pyperclip.copy(content)
        textbox.send_keys(Keys.CONTROL + "a")
        textbox.send_keys(Keys.CONTROL + "v")
    # publish the page
    driver.find_element_by_id(getID(driver, "ctl00_ContentPlaceHolder1_ctl00_ibPublishBottom")).click()
    if not isOldPage:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, getID(driver, "ctl00_ContentPlaceHolder1_ctl00_btnYes"))))
        driver.find_element_by_id(getID(driver, "ctl00_ContentPlaceHolder1_ctl00_btnYes")).click()
    isOldPage= False
    
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

# initial setup: start Firefox and login to website
driver = webdriver.Firefox()
driver.get("http://stockton.ss7.sharpschool.com/gateway/Login.aspx?returnUrl=%2fcms%2fOne.aspx%3fportalId%3d462272%26pageId%3d3526277")
driver.find_element_by_name("ctl00$ContentPlaceHolder1$txtUsername").send_keys(input("Username: "))
driver.find_element_by_name("ctl00$ContentPlaceHolder1$txtPassword").send_keys(input("Password: "))
driver.find_element_by_name("ctl00$ContentPlaceHolder1$btnLogin").click()

excelLine = "-1"
commaCount = 0
currCommaCount = -1
pagePath = []

#currPage = input("Please enter the URL of the SharpSchool site which you would like to create the pages on: ")
currPage = "http://stockton.ss7.sharpschool.com/cms/One.aspx?portalId=462272&pageId=3526277"
pagePath.append(currPage)

# Open the .csv file which contains the website skeleton
# excelSheet = open(input("Please enter the file name: "), "r")
excelSheet = open("ONC.csv", "r")
divName = input("Please enter the class or ID name of the div which contains the content on the old site: ")

# Creates all pages on the .csv file
while True:
    # variable reset
    isOldPage = False    
    
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
        ext_page(excelLine)
    # Create all other types of pages
    else:
        # Separate page name and old site URL
        name, link = excelLine.rsplit(',', 1)
        name = name.strip(' ,"')
        link = link.strip(' ,"')
        name = name.replace("\"\"","\"")
        enter_title(name)
        
    # if ext link page or blog page, it ends up on the parent page
    if pageChar == '1' or pageChar == '9': 
        pagePath.pop()
        currCommaCount = currCommaCount - 1    
    # if content space page or teacher page, there is a 2nd step
    elif pageChar == '0' or pageChar == '8':
        content_page(link)
        
    pagePath.append(driver.current_url)

excelSheet.close()
print("done! :D")