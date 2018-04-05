import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select
import time
import glob
import shutil


import urllib.request
import csv
import datetime
import sys


class TWDB_Scraper(object):
    def __init__(self,weblink):
        self.url = weblink
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.delay = 3 # of seconds to wait
        
    def load_page(self):
        self.driver.get(self.url)
        try:
            wait = WebDriverWait(self.driver, self.delay)
            wait.until(EC.presence_of_all_elements_located((By.ID,"headID")))
            print("page is ready")
        except TimeoutException:
            print("loading took too much time") 
            
    def get_all_options(self):
        select_box = Select(self.driver.find_element_by_id("ReportViewerControl_ctl04_ctl03_ddValue"))
        all_options = [x.text for x in select_box.options]
        #print(len(all_options))
        return(all_options)
            
    def select_item(self,item_to_select):
        select_box = Select(self.driver.find_element_by_id("ReportViewerControl_ctl04_ctl03_ddValue"))
        time.sleep(1)
        #print(dropdown_web_element)
        try:
            select_box.select_by_visible_text(item_to_select)
            self.driver.find_element_by_name("ReportViewerControl$ctl04$ctl00").click()
            
            wait = WebDriverWait(self.driver, self.delay)
            wait.until(EC.presence_of_all_elements_located((By.ID,"ReportViewerControl_ctl05_ctl04_ctl00_ButtonLink")))
            print("select item successfully, data ready to be downloaded")
        except:
            print("select item NOT successfully, check if item exists in the dropdown menue")
            
    def download_excel(self):
        
        time.sleep(12)
        try:
            self.driver.find_element_by_id("ReportViewerControl_ctl05_ctl04_ctl00_ButtonLink").click()
            self.driver.find_element_by_xpath("//*[@title='Excel']").click()
            print("download sucessful")
        except:
            print("download failed")
        time.sleep(7)
            
    def turnoff_driver(self):
        time.sleep(7)
        self.driver.quit()
        print('turn off driver after job done')

os.chdir(r'C:\Users\markp\Desktop\WaterSurvey')

weblink=f"http://www2.twdb.texas.gov/ReportServerExt/Pages/ReportViewer.aspx?%2fWU%2fSumFinal_CountyPumpage&rs:Command=Render"
# item_to_select="2015"
sourcedir=r'C:\Users\markp\Downloads'
destdir=r'C:\Users\markp\Desktop\WaterSurvey\data'
filename="SumFinal_CountyPumpage.xlsx"

## Downloading ##

scraper = TWDB_Scraper(weblink)
scraper.load_page()

all_options = scraper.get_all_options()
all_options = [x for x in all_options if x != '<Select a Value>']
test_options = all_options[98:len(all_options)]

os.chdir(sourcedir)

count=101
for option in all_options[102:]:
    count=count+1
    scraper.select_item(option)
    scraper.download_excel()
    print('data for ' +option+ ' downloaded, ' +str(count)+' out of '+ str(len(all_options)))
    try:
        os.rename(filename,'countypump_'+option+'.xlsx')
        print('rename finished')
    except:
        print('rename failed')
    
scraper.turnoff_driver()

for filename in glob.glob(os.path.join(sourcedir, '*.xlsx')):
    shutil.move(filename, destdir)

## After downloading ##

# create a folder to save the data and copy in data from download folder


    
# =============================================================================
# os.chdir(destdir)
# 
# def sorted_ls(path):
#     mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
#     return list(sorted(os.listdir(path), key=mtime))
# 
# for f, newf in zip(sorted_ls(destdir),all_options[0:101]):
#     os.rename(f,"countypump_"+newf+'.xlsx')
# =============================================================================
    
