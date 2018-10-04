# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 14:51:01 2018

@author: SHRIKRISHNA
"""

#add exception and wait time


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException 
import time

link = []

#driver = webdriver.Chrome('chromedriver.exe')
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
ff_Binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
driver = webdriver.Firefox(firefox_binary = ff_Binary)

try:
    driver.set_page_load_timeout(10)
    driver.get("https://zomato.com")
    driver.maximize_window()
except TimeoutException as ex:
    isrunning = 0
    print("Exception has been thrown. " + str(ex))
    driver.close()

#LOCATING ELEMENT
    
element = driver.find_element_by_xpath('//*[@id="location_contianer"]')
time.sleep(4)
element.click() 
ele_inp = driver.find_element_by_xpath('//*[@id="location_input"]')
ele_inp.send_keys("Pune")
time.sleep(1)
ele_inp.send_keys(Keys.ARROW_DOWN)
#time.sleep(2)
ele_inp.click()
ele_inp.send_keys(Keys.ENTER)
time.sleep(5)

elem_search = driver.find_element_by_xpath('//*[@id="keywords_input"]')
#elem_search.click()
elem_search.send_keys("McDonald's")
time.sleep(5)
#elem_search.send_keys(Keys.RETURN)
elem_search.send_keys(Keys.ARROW_DOWN)
time.sleep(2)
driver.find_element_by_xpath('//*[@id="search_button"]').click()
time.sleep(4)

url = driver.current_url
print(url)
#driver.refresh()

#Storing page links in P_link

p_link = []      
for p in driver.find_elements_by_class_name("paginator_item"):
    if p not in p_link:
        p_link.append(p.get_attribute("href"))


# Getting each McDonal's link's in link 
        
for url in range (1,len(p_link)-1):
    driver.get(p_link[url])
    time.sleep(5)
    for a in driver.find_elements_by_class_name("result-title"):
        link.append(a.get_attribute("href"))
        
print ("NUMBER OF LINKS AVAILABLE IS " + str(len(link)))
  
# Opening .csv file to write our data in it 

filename = "Details.csv"
f = open(filename, "w",encoding = "utf-8")
headers = "Name , Phone, Address, Reviewer Name, Review Score, Review Text, Link \n"
f.write(headers)


#Looping through each link, Extract data and write them in our desire file 

for i in range (0 , len(link)):
        
    driver.get(link[i])
    time.sleep(5)
    
    Name = driver.find_element_by_class_name("res-name").text
    
    Phone = driver.find_element_by_class_name("tel").text.replace("\n", " ")
    f_Phone= "0" +Phone[3:]
    
    Address = driver.find_element_by_class_name("resinfo-icon").text
    Address = Address.replace(","," ")
      
    Reviewer_Name = driver.find_element_by_class_name("item .header").text
    
    a = driver.find_element_by_class_name("rev-text .ttupper")
    Review_Score  = a.get_attribute("aria-label")
    
    try:
        driver.find_element_by_class_name("read-more").click()
    except NoSuchElementException :
        pass
    
    Review = driver.find_element_by_class_name("rev-text").text.replace("\n", " ")
    Review = Review[5:].strip().replace(",", " ")
    
    f.write(Name + "," +f_Phone +"," + Address +","+ Reviewer_Name +", "+ Review_Score +","+Review +"," +link[i] +" \n")
    
# Closing file
    
f.close()

print ("DATA HAS BEEN WRITTEN IN " + filename)

print ("Procedure completed! See " + filename )


driver.close()