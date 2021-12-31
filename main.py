from tkinter import Tk   
from tkinter.filedialog import askopenfilename,asksaveasfile
import os.path
from nameparser.parser import group_contiguous_integers
Tk().withdraw() 
filename = askopenfilename()

import pandas as pd

df=pd.read_csv(filename,encoding="windows-1252")
df=df.fillna("")
import time
import random
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
options=webdriver.ChromeOptions()
prefs={"profile.default_content_setting_values.notifications":2}
options.add_experimental_option("prefs",prefs)
options.add_argument("start-maximized")
options.add_argument("--disable-notifications")
options.add_argument("--disable-infobars")
options.add_experimental_option('excludeSwitches', ['enable-logging','enable-automation'])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument('--dns-prefetch-disable')

from webdriver_manager.chrome import ChromeDriverManager
browser = webdriver.Chrome(ChromeDriverManager().install(),options=options)
not_inc=[]
browser.get("http://www.linkedin.com/login/")
time.sleep(random.uniform(2.5, 4.9))
try:
   WebDriverWait(browser, 2000).until(EC.presence_of_element_located((By.XPATH, "//div[@class='t-16 t-black t-bold']"))).text.strip()   
except:
    pass
urls=[]
for i in range(1,len(df)):
    print(i)
    try:
        
        first=df['First Name'].iloc[i]
        last=df['Last Name'].iloc[i]
        comp=df['Company'].iloc[i]
        import re
        pos=df['Position'].iloc[i]
    except:
        pass    
    try:
        pos=re.sub('[-!\/|@#$%^&*+_?><]', ' ', pos)
    except:
        pass  
    
    try:   
        link="https://www.linkedin.com/search/results/people/?firstName="+first+"%20%20&lastName="+last+"%20&origin=FACETED_SEARCH"
        browser.get(link)
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Keywords filter. 2 Keywords filters are applied. Clicking this button displays all Keywords filter options.']"))).click()
        hover1=WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='artdeco-hoverable-content artdeco-hoverable-content--visible reusable-search-filters-trigger-dropdown__content artdeco-hoverable-content--inverse-theme artdeco-hoverable-content--default-spacing artdeco-hoverable-content--bottom-placement']")))
        ul1=hover1.find_element_by_xpath(".//ul[@class='list-style-none display-flex flex-wrap flex-column']")
        l1=ul1.find_elements_by_tag_name("li")
        input1=l1[2].find_element_by_xpath(".//input[@class='mt1']")
        input1.send_keys(pos)
        check1=WebDriverWait(hover1, 10).until(EC.presence_of_element_located((By.XPATH, ".//div[@class='reusable-search-filters-buttons display-flex justify-flex-end mt3 ph2']")))
        WebDriverWait(check1, 10).until(EC.presence_of_element_located((By.XPATH, ".//button[@data-control-name='filter_show_results']"))).click()
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Current company filter. Clicking this button displays all Current company filter options.']"))).click()
        hover=WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='artdeco-hoverable-content artdeco-hoverable-content--visible reusable-search-filters-trigger-dropdown__content artdeco-hoverable-content--inverse-theme artdeco-hoverable-content--default-spacing artdeco-hoverable-content--bottom-placement']")))
        try:
            
            ul=hover.find_element_by_xpath(".//ul[@class='list-style-none relative search-reusables__collection-values-container search-reusables__collection-values-container--50vh']")
            input_btn=WebDriverWait(ul, 10).until(EC.presence_of_element_located((By.XPATH, ".//li[@class='search-reusables__collection-values-item']")))
            check_box=input_btn.find_element_by_xpath(".//input[@data-control-name='filter_detail_select']")
            browser.execute_script("arguments[0].click();", check_box)
            check=WebDriverWait(hover, 10).until(EC.presence_of_element_located((By.XPATH, ".//div[@class='reusable-search-filters-buttons display-flex justify-flex-end mt3 ph2']")))
            WebDriverWait(check, 10).until(EC.presence_of_element_located((By.XPATH, ".//button[@data-control-name='filter_show_results']"))).click()
            try:
                links=WebDriverWait(browser, 4).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='entity-result__content entity-result__divider pt3 pb3 t-12 t-black--light']")))
                for l in links:
                        urls.append(l.find_element_by_xpath(".//a[@class='app-aware-link']").get_attribute("href").split('?')[0]+'/')
            except:
                    name=first+' '+last
                    not_inc.append({'Name':name,'Current comp':comp})
                        
        
        except:
            ul_in=hover.find_element_by_xpath(".//input[@placeholder='Add a company']")
            ul_in.send_keys(comp)
            time.sleep(random.uniform(2.5, 4.9))
            try:
                u_list=browser.find_element_by_xpath(".//div[@role='listbox']")
                c_list=u_list.find_element_by_xpath(".//*")
                c_list.find_element_by_xpath(".//*").click()
            except:
                pass    
            check=WebDriverWait(hover, 10).until(EC.presence_of_element_located((By.XPATH, ".//div[@class='reusable-search-filters-buttons display-flex justify-flex-end mt3 ph2']")))
            WebDriverWait(check, 10).until(EC.presence_of_element_located((By.XPATH, ".//button[@data-control-name='filter_show_results']"))).click()
            try:
                links=WebDriverWait(browser, 4).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='entity-result__content entity-result__divider pt3 pb3 t-12 t-black--light']")))
                for l in links:
                        urls.append(l.find_element_by_xpath(".//a[@class='app-aware-link']").get_attribute("href").split('?')[0]+'/')
            except:
                    name=first+' '+last
                    not_inc.append({'Name':name,'Current comp':comp})
    except:
        name=first+' '+last
        not_inc.append({'Name':name,'Current comp':comp})                       

browser.quit()   
    

urls=sorted(list(set(urls)))

def file_save():
    try:
        
        f = asksaveasfile(mode='w', initialfile=os.path.basename(filename).split(".")[0]+"_connections"+".txt", defaultextension=".txt")
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
    
        for i in urls:
            f.write(str(i)+'\r\n')
        f.close()
        pass
    except:
        pass
       
file_save()
# def file_save2():
#     try:
        
#         f = asksaveasfile(mode='w', initialfile=os.path.basename(filename).split(".")[0]+"_not_included"+".txt", defaultextension=".txt")
#         if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
#             return
    
#         for i in not_inc:
#             f.write(str(i)+'\r\n')
#         f.close()
#         pass
#     except:
#         pass
       
# file_save2()





