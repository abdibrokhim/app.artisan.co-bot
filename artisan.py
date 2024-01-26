import time,math,random,os
import utils,config
import pickle, hashlib

from selenium import webdriver
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

import pandas as pd
from helper import append_to_excel, append_to_csv, backup_append_to_csv

class Artisan:
    def __init__(self):
            utils.prYellow("🌐 Bot will run in Chrome browser and log in Artisan for you.")
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=utils.chromeBrowserOptions())
            self.cookies_path = f"{os.path.join(os.getcwd(),'cookies')}/{self.getHash(config.email)}.pkl"
            self.driver.get('https://app.artisan.co/leads')
            self.loadCookies()

            if not self.isLoggedIn():
                self.driver.get("https://app.artisan.co/login")
                utils.prYellow("🔄 Trying to log in Artisan...")
                try:    
                    self.driver.find_element("xpath",'//*[@id="root"]/div/div[1]/div[2]/div/div/div/div/div[2]/div[1]/form/div/div/input').send_keys(config.email)
                    time.sleep(2)
                    self.driver.find_element("xpath",'//*[@id="root"]/div/div[1]/div[2]/div/div/div/div/div[2]/div[1]/form/div/button').click()
                    time.sleep(50)

                    # let's fiil out OTP
                    # get input OTP
                    utils.prYellow("🔄 Waiting for OTP...")
                    otp = input("Enter OTP: ")
                    print('otp: ', otp)

                    self.driver.find_element("xpath",'//*[@id="root"]/div/div[1]/div[2]/div/div/div/div/div[2]/div/form/div/div[1]/div/input[1]').send_keys(int(otp[0]))
                    self.driver.find_element("xpath",'//*[@id="root"]/div/div[1]/div[2]/div/div/div/div/div[2]/div/form/div/div[1]/div/input[2]').send_keys(int(otp[1]))
                    self.driver.find_element("xpath",'//*[@id="root"]/div/div[1]/div[2]/div/div/div/div/div[2]/div/form/div/div[1]/div/input[3]').send_keys(int(otp[2]))
                    self.driver.find_element("xpath",'//*[@id="root"]/div/div[1]/div[2]/div/div/div/div/div[2]/div/form/div/div[1]/div/input[4]').send_keys(int(otp[3]))
                    self.driver.find_element("xpath",'//*[@id="root"]/div/div[1]/div[2]/div/div/div/div/div[2]/div/form/div/div[1]/div/input[5]').send_keys(int(otp[4]))
                    self.driver.find_element("xpath",'//*[@id="root"]/div/div[1]/div[2]/div/div/div/div/div[2]/div/form/div/div[1]/div/input[6]').send_keys(int(otp[5]))
                    time.sleep(2)

                    # click on submit button
                    utils.prYellow("🔄 Submitting OTP...")
                    time.sleep(2)
                    # click checkbox
                    self.driver.find_element("xpath",'//*[@id="root"]/div/div[1]/div[2]/div/div/div/div/div[2]/div/form/div/div[2]/div/div/span/input').click()
                    time.sleep(2)
                    self.driver.find_element("xpath",'//*[@id="root"]/div/div[1]/div[2]/div/div/div/div/div[2]/div/form/div/button').click()
                    time.sleep(30)
                    utils.prGreen("✅ Logged in Artisan successfully.")
                except:
                    utils.prRed("❌ Couldn't log in Artisan by using Chrome.")

                self.saveCookies()
            # start application
            self.scrape_leads()

    def getHash(self, string):
        return hashlib.md5(string.encode('utf-8')).hexdigest()

    def loadCookies(self):
        if os.path.exists(self.cookies_path):
            cookies =  pickle.load(open(self.cookies_path, "rb"))
            self.driver.delete_all_cookies()
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    def saveCookies(self):
        pickle.dump(self.driver.get_cookies() , open(self.cookies_path,"wb"))
    
    def isLoggedIn(self):
        self.driver.get('https://app.artisan.co/leads')
        try:
            self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr[2]/td[1]/div/p')
            return True
        except:
            pass
        return False 
    

    # open new xls file
    def openXls(self,):
        utils.prGreen("✅ Opening xls file...")
        time.sleep(2)
        pass


    def scrape_leads(self,):
        utils.prGreen("✅ Opening leads tab...")
        self.driver.get('https://app.artisan.co/leads')

        utils.prGreen("✅ Scraping leads...")
        time.sleep(2)

        leadNames = []
        leadEmails = []
        leadStatus = []
        leadCompany = []
        leadWorkflowStage = []
        leadLastContact = []
        leadIndustry = []
        leadNumberOfEmployees = []
        leadLinkedin = []
        leadEmailOpens = []
        leadLinkClicks = []
        leadLocalTime = []
        leadLocation = []
        leadFoundedYear = []
        leadWebsite = []
        leadDescription = []

        tatolPages = self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div/div[3]/div[1]/nav/ul/li[8]/button').text
        print('tatolPages: ', tatolPages)

        j = 2
        n = int(input("Enter page number: "))

        utils.prYellow("🔄 Going to processing page...")
        time.sleep(2)
        for _ in range(0, n-1):
            self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div/div[3]/div[1]/nav/ul/li[9]/button').click()
            time.sleep(6)
        time.sleep(6)

        for i in range(n, int(tatolPages)+1):
            utils.prYellow("🔄 Scraping page: " + str(i))
            time.sleep(2)
            
            totalLeads = len(self.driver.find_elements(By.XPATH,f'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td[1]/div/p'))
            for k in range(1, totalLeads+1):
                print('totalLeads: ', totalLeads)
                utils.prYellow("🔄 Scraping lead: " + str(k))

                time.sleep(2)
                leadNames.append(self.driver.find_element(By.XPATH,f'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr[{j}]/td[1]/div/p').text)
                time.sleep(2)
                leadEmails.append(self.driver.find_element(By.XPATH,f'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr[{j}]/td[2]/p').text)
                time.sleep(2)
                leadStatus.append(self.driver.find_element(By.XPATH,f'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr[{j}]/td[3]/p').text)
                time.sleep(2)
                leadCompany.append(self.driver.find_element(By.XPATH,f'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr[{j}]/td[4]/p').text)
                time.sleep(2)
                leadWorkflowStage.append(self.driver.find_element(By.XPATH,f'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr[{j}]/td[5]/p').text)
                time.sleep(2)

                lastContact = self.driver.find_element(By.XPATH,f'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr[{j}]/td[6]/p').text if \
                    self.driver.find_element(By.XPATH,f'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr[{j}]/td[6]/p').text else "-"
                leadLastContact.append(lastContact)
                time.sleep(2)
                
                utils.prYellow("🔄 Scraping individual leads info...")
                self.driver.find_element(By.XPATH,f'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr[{j}]').click()
                time.sleep(6)
                
                description = self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div[1]/div/div[1]/p').text if \
                    self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div[1]/div/div[1]/p').text else "-"
                leadDescription.append(description)
                time.sleep(2)
                
                website = self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div[1]/div/div[2]/div[1]/a/p').text if \
                    self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div[1]/div/div[2]/div[1]/a/p').text else "-"
                leadWebsite.append(website)
                time.sleep(2)

                foundedYear = self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div[1]/div/div[2]/div[2]/h2[2]').text if \
                    self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div[1]/div/div[2]/div[2]/h2[2]').text else "-"
                leadFoundedYear.append(foundedYear)
                time.sleep(2)

                industry = self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div[1]/div/div[3]/h2[2]').text if \
                    self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div[1]/div/div[3]/h2[2]').text else "-"
                leadIndustry.append(industry)
                time.sleep(2)

                numberOfEmployees = self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div[1]/div/div[4]/h2[2]').text if \
                    self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div[1]/div/div[4]/h2[2]').text else "-"
                leadNumberOfEmployees.append(numberOfEmployees)
                time.sleep(2)

                linkedin = self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div[2]/div[1]/a[2]').text if \
                    self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div[2]/div[1]/a[2]').text else "-"
                leadLinkedin.append(linkedin)
                time.sleep(2)

                emailOpens = self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div[2]/div[2]/div[1]/h2[2]').text
                leadEmailOpens.append(emailOpens)
                time.sleep(2)

                clicks = self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div[2]/div[2]/div[2]/h2[2]').text
                leadLinkClicks.append(clicks)
                time.sleep(2)

                location = self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div[2]/div[3]/div[1]/h2[2]').text
                leadLocation.append(location)
                time.sleep(2)

                localTime = self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div[2]/div[3]/div[2]/h2[2]').text
                leadLocalTime.append(localTime)
                time.sleep(2)

                utils.prYellow("🔄 Scraping individual leads info finished.")
                time.sleep(2)

                # go back to leads page
                utils.prYellow("🔄 Going back to leads page...")
                time.sleep(2)
                self.driver.get('https://app.artisan.co/leads')
                time.sleep(6)
                j += 1

                # save data to backup csv file
                utils.prYellow("🔄 Saving data to backup csv file...")
                data = {
                    'Name': [leadNames[-1]],
                    'Email': [leadEmails[-1]],
                    'Status': [leadStatus[-1]],
                    'Company': [leadCompany[-1]],
                    'Workflow Stage': [leadWorkflowStage[-1]],
                    'Last Contact': [leadLastContact[-1]],
                    'Industry': [leadIndustry[-1]],
                    'Number of Employees': [leadNumberOfEmployees[-1]],
                    'Linkedin': [leadLinkedin[-1]],
                    'Email Opens': [leadEmailOpens[-1]],
                    'Link Clicks': [leadLinkClicks[-1]],
                    'Local Time': [leadLocalTime[-1]],
                    'Location': [leadLocation[-1]],
                    'Founded Year': [leadFoundedYear[-1]],
                    'Website': [leadWebsite[-1]],
                    'Description': [leadDescription[-1]]
                }
                print('data: ', data)
                try:
                    backup_append_to_csv(config.backup_csv_path, data)
                    utils.prGreen("✅ Saved data to backup csv file.")
                    print('This data: ', data)
                except:
                    utils.prRed("❌ Couldn't save data to backup csv file.")
                    print('This data: ', data)

                if i > 1:
                    utils.prYellow("🔄 Going Back to processing page...")
                    time.sleep(2)
                    for _ in range(0, i-1):
                        self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div/div[3]/div[1]/nav/ul/li[9]/button').click()
                        time.sleep(6)
                    time.sleep(6)

            utils.prYellow("🔄 Going to next page...")
            time.sleep(2)
            self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div/div/div/div/div[3]/div[1]/nav/ul/li[9]/button').click()
            j = 2
            time.sleep(6)
                


        # save data to csv file
        utils.prYellow("🔄 Saving data to csv file...")

        data = {
            'Name': leadNames,
            'Email': leadEmails,
            'Status': leadStatus,
            'Company': leadCompany,
            'Workflow Stage': leadWorkflowStage,
            'Last Contact': leadLastContact,
            'Industry': leadIndustry,
            'Number of Employees': leadNumberOfEmployees,
            'Linkedin': leadLinkedin,
            'Email Opens': leadEmailOpens,
            'Link Clicks': leadLinkClicks,
            'Local Time': leadLocalTime,
            'Location': leadLocation,
            'Founded Year': leadFoundedYear,
            'Website': leadWebsite,
            'Description': leadDescription
        }
        try:
            append_to_csv(config.csv_path, data)
            utils.prGreen("✅ Saved data to csv file.")
        except:
            utils.prRed("❌ Couldn't save data to csv file.")

        utils.prGreen("✅ Scraping finished successfully.")
    

start = time.time()
Artisan()
end = time.time()
utils.prYellow("---Took: " + str(round((time.time() - start)/60)) + " minute(s).")
