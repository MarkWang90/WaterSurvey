# WaterSurvey

The project used Python and selenium to get data from TWBD websites [(click here)](http://www2.twdb.texas.gov/ReportServerExt/Pages/ReportViewer.aspx?%2fWU%2fSumFinal_CountyPumpage&rs:Command=Render). The major code is in file **watersurvey.py**. As you can see in the webpage, TWBD manages their databasethrough Microsoft SQL server. To get the county-level water use data for all counties in Texas, we have to select the county from the dropdown menu and click download one by one (and there are 254 counties in Texas). Thus, an automated procedures is develop utilizing the web testing tool selenium with Python for this purpose.


The code is in **watersurvey.py** with a class defined as TWDB_Scrapter and several **functions** which are self-explainary:

1. **load_page**: loads the TWDB websites
2. **get_all_options**: get all options (counties) from the dropdown menu and save it in a list
3. **select_item**: select one option
4. **download_excel**: click the button to generate and download the data into a excel file
5. **turnoff_driver**: turn off the webdriver

Then, the automated procedure could be accomplised the loop as below:

```python

## set up working direct and weblinks ##
os.chdir(r'C:\Users\markp\Desktop\WaterSurvey')
weblink=f"http://www2.twdb.texas.gov/ReportServerExt/Pages/ReportViewer.aspx?%2fWU%2fSumFinal_CountyPumpage&rs:Command=Render"
sourcedir=r'C:\Users\markp\Downloads'
destdir=r'C:\Users\markp\Desktop\WaterSurvey\data'
filename="SumFinal_CountyPumpage.xlsx"

## Initialize the driver, get all counties in a list ##
scraper = TWDB_Scraper(weblink)
scraper.load_page()
all_options = scraper.get_all_options()
all_options = [x for x in all_options if x != '<Select a Value>']
test_options = all_options[98:len(all_options)]

## loop downloading ##
os.chdir(sourcedir)
count=0
for option in all_options[1:]:
    count=count+1
    scraper.select_item(option)
    scraper.download_excel()
    print('data for ' +option+ ' downloaded, ' +str(count)+' out of '+ str(len(all_options)))
    try:
        os.rename(filename,'countypump_'+option+'.xlsx')
        print('rename finished')
    except:
        print('rename failed')
        
## turn off driver after finish ##    
scraper.turnoff_driver()

## copy the file from download folder to destination folder ##
for filename in glob.glob(os.path.join(sourcedir, '*.xlsx')):
    shutil.move(filename, destdir)

```
