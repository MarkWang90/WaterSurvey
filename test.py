from selenium import webdriver
from selenium.webdriver.support.select import Select
import time

url = f"http://www2.twdb.texas.gov/ReportServerExt/Pages/ReportViewer.aspx?%2fWU%2fSumFinal_CountyReportWithReuse&rs:Command=Render"
        
driver = webdriver.Chrome()
driver.get(url)

select_box = Select(driver.find_element_by_id("ReportViewerControl_ctl04_ctl03_ddValue"))
select_box.select_by_visible_text("2015")

view_report = driver.find_element_by_name("ReportViewerControl$ctl04$ctl00").click()
click_download = driver.find_element_by_id("ReportViewerControl_ctl05_ctl04_ctl00_ButtonLink").click()
choose_excel = driver.find_element_by_xpath("//*[@title='Excel']").click()
