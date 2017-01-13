import urllib2
import urllib
from bs4 import BeautifulSoup
from selenium import webdriver
import sqlite3
from random import randint
from time import sleep

conn = sqlite3.connect('bayarea_housing.db')
c = conn.cursor()
c.execute("DROP TABLE housing_price")
c.execute('''CREATE TABLE housing_price
             (ID integer
             , county text, address text, city text, zipcode text, sale_date text, sale_price integer
             , detail_link text, scrape_url text
             , PRIMARY KEY (address, sale_date))''')

driver = webdriver.Firefox()
SessionID= "60035670489407134505196209674346758940388447344978505886011557138167728185250616879073525788828204892079524594106107795619659181"
for cpipage in range(1,11):
    url = "http://www.sfgate.com/webdb/homesales/?appSession="+SessionID+"&PageID=2&PrevPageID=1&cpipage="+str(cpipage)+"&CPISortType=&CPIorderBy="
    print url
    driver.get(url)
    # confirm table exists
    assert "data-cb-name" in driver.page_source, "page source not loaded correctly"

    # get all table values
    elems = driver.find_elements_by_xpath("//tr[@data-cb-name='data']/td")
    links = driver.find_elements_by_xpath("//a[@data-cb-name='DetailsLink']")

    # insert into db
    for i in range(0,len(elems)/8):
        county = elems[8*i].text
        address = elems[8*i+1].text
        city = elems[8*i+2].text
        zipcode = elems[8*i+3].text
        sale_date = elems[8*i+4].text
        sale_price = elems[8*i+5].text.replace("$","").replace(",","")
        nrow = str(c.execute("SELECT COUNT(1) AS cnt FROM housing_price").fetchone()[0])
        row = "\",\"".join([nrow, county,address,city,zipcode,sale_date,sale_price,detail_link,url])
        c.execute("INSERT INTO housing_price VALUES (\"" + row + "\")")

    conn.commit()
conn.close()

driver.close()    
