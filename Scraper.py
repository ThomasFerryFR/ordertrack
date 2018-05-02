import pandas as pd
from bs4 import BeautifulSoup as BS
import requests
import selenium
from selenium import webdriver

# MAEU8358826

class order:

    def __init__(self,nameOrder,poNum,containerNum, carrier, dueDate):
        self.name = nameOrder
        self.po = poNum
        self.cont = containerNum
        self.carrier = carrier
        self.dueDate = dueDate
        self.etaDate = "Unknown -Not Fetched"

    def extract_status(self):
        """Lorem Ipsum"""
        url = "https://my.maerskline.com/tracking/search?keyType=UNKNOWN_TYPE&searchNumber={}".format(self.cont)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        #The line above is to get around webscraping prevention some websites might have in place.
        
        print('Fetching Status Data...')
        
        browser = webdriver.Firefox()
        browser.get(url) 
        innerHTML = browser.execute_script("return document.body.innerHTML")
        browser.stop_client()
        browser.close()
        
        parser = BS(innerHTML, 'html.parser')

        # -------------------------------------------
        # Extracting the status
        # -------------------------------------------
        finalEta = list()
        span_tag = parser.findAll('span', attrs={"class":"ETA-block"})
        
        # -------------------------------------------
        # Cleaning the report adresses
        # -------------------------------------------
        status = list()
        dateEta = list()
        for tag in span_tag:    
            status.append(tag.text)
            dateEta.append(tag.text.split('\n                ',2)[1])
        
        self.etaDate = dateEta[0]

        return {"Full Status":status,"Estimated Arrival Date:":dateEta}

test_order = order('Test',1234567890,'MAEU8358826','MaerskLine','06/02/2018')

print(test_order.etaDate)
test_order.extract_status()
print(test_order.etaDate)