from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import pyperclip
import os
import re

class facebookFill:

    driver = object()
    ft_status = 0
    index=0
    profile_path=os.path.abspath('./Profiles/Default')
    folderpath = 'AdsData/'


    def __init__(self, path,adspath='./AdsData/'):
        self.profile_path = path
        self.folderpath = adspath
        
    # 指定使用Chrome浏览器
    def launchbrowser(self):
        try:
            #配置浏览器启动选项
            option = webdriver.ChromeOptions()
            service = Service(executable_path='./Driver/chromedriver.exe')
            prefs = {
                'profile.default_content_setting_values':
                    {
                        'notifications': 2
                    }
            }
            option.add_experimental_option('prefs',prefs)
            option.add_experimental_option('detach',True)
            option.add_argument("disable-infobars")
            option.add_argument(r'user-data-dir='+self.profile_path)#这里是用户profile的设置，默认使用的值是default文件夹。
            
            self.driver = webdriver.Chrome(options=option,service=service)#调用的浏览器路径
        except Exception as e:
            raise e

        # 打开网页
        self.driver.get("https://www.facebook.com/")

        #浏览器启动之后把状态设成1，表示浏览器运行中
        self.ft_status=1

    def set_folderpath(self,adspath):
        self.folderpath = adspath


    def autofill(self):
        self.driver.get("https://www.facebook.com/marketplace/create/item")

        titletxt = "Workbench"
        pricetxt = "1080"
        desctxt = "xxx:1080,xxxx:1050:xxxx1020"
        catetxt = "Tools"


        #文案读取
        with open(self.folderpath+'title.txt','r', encoding="utf-8") as titlef:
            titletxt = titlef.read()

        with open(self.folderpath+'price.txt','r') as pricef:
            pricetxt = pricef.read()

        with open(self.folderpath+'desc.txt','r', encoding="utf-8") as descf:
            desctxt = descf.read()
        
        with open(self.folderpath+'tags.txt','r', encoding="utf-8") as tagf:
            raw_tags = tagf.read()
        
        with open(self.folderpath+'cate.txt', 'r') as catef:
            catetxt = catef.read()
            catetxt.strip()


        #控件定位
        inputs = self.driver.find_elements(By.CSS_SELECTOR,"div[role='main'] input[type='text']")
        title = inputs[0]
        price = inputs[1]
        dropdown = self.driver.find_elements(By.CSS_SELECTOR,"div[role='main'] div[role='button'][aria-expanded='false']")
        dropdown = dropdown[0]
        time.sleep(1)
        dropdown.click()

        
        #选择condition
        condi = self.driver.find_elements(By.CSS_SELECTOR,"div[role='main'] label[aria-label='Condition']")[0]
        condi.click()
        newopt = self.driver.find_elements(By.CSS_SELECTOR,"div[role='listbox'] div[role='option']")[0]
        newopt.click()

        #选择stock
        ava = self.driver.find_elements(By.CSS_SELECTOR,"div[role='main'] label[aria-label='Availability']")[0]
        ava.click()
        stockopt = self.driver.find_elements(By.CSS_SELECTOR,"div[role='listbox'] div[role='option']")[1]
        stockopt.click()

        #定位控件2
        description = self.driver.find_elements(By.CSS_SELECTOR,"div[role='main'] textarea[rows='4']")[0]
        tags = self.driver.find_elements(By.CSS_SELECTOR,"div[role='main'] textarea[rows='1']")[0]
        print(description)
        print(tags)

        #选择category
        cate = self.driver.find_elements(By.CSS_SELECTOR,"div[role='main'] label[aria-label='Category']")[0]
        cate.click()
        cateopt = self.driver.find_elements(By.CSS_SELECTOR,"div[role='dialog'] div[role='button'] span")
        misc = []
        for i in cateopt:
            if catetxt in i.text:
                misc = i
                break
        misc.click()


        price.send_keys(pricetxt)
        
        pyperclip.copy(desctxt)
        description.send_keys(Keys.CONTROL,"v")
        
        pyperclip.copy(raw_tags)
        tags.send_keys(Keys.CONTROL,"v")
        tags.send_keys(Keys.ENTER)


        pyperclip.copy(titletxt)
        title.send_keys(Keys.CONTROL,"v")
        
    def autolist(self):
        inputs = self.driver.find_elements(By.CSS_SELECTOR,"div[aria-label='List in More Places'] div:not([aria-label])[role='button']")
        items = inputs[self.index:]
        print(len(items))
        if len(items)==0:
            self.index=0
            raise Exception("No Items")
        for i in items:
            if bool(i.get_attribute('aria-label')):
                continue
            if bool(i.get_attribute('aria-disabled')):
                break
            i.click()
            self.index = self.index+1

    def autoupdate(self):
        #进入编辑页面并读取城市名
        partern = r'([\w\s\'-]+),\s*(ON|QC|AB|NB)'
        Cityname = ''
        Provincename = ''
        Links= self.driver.find_elements(By.CSS_SELECTOR,"div[aria-label='Your Listing'] a[role='link'][href]")
        for i in Links:
            matches = re.findall(partern,i.text)
            if bool(matches):
                Cityname = matches[0][0].strip()
                Provincename = matches[0][1][0].strip()
                break
        
        location_str = Cityname+','+Provincename
        
        editlist = self.driver.find_elements(By.CSS_SELECTOR,"div[aria-label='Your Listing'] a[aria-label='Edit Listing']")[0]
        editlist.click()

        element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div[role='main'] input[type='text'][aria-label='Location']")))

        titletxt = "Workbench"
        pricetxt = "1080"
        desctxt = "xxx:1080,xxxx:1050:xxxx1020"
        catetxt = "Tools"

        #文案读取
        with open(self.folderpath+'title.txt','r', encoding="utf-8") as titlef:
            titletxt = titlef.read()

        with open(self.folderpath+'price.txt','r') as pricef:
            pricetxt = pricef.read()

        with open(self.folderpath+'desc.txt','r', encoding="utf-8") as descf:
            desctxt = descf.read()
        
        with open(self.folderpath+'tags.txt','r', encoding="utf-8") as tagf:
            raw_tags = tagf.read()
        
        with open(self.folderpath+'cate.txt', 'r') as catef:
            catetxt = catef.read()
            catetxt.strip()


        #控件定位
        
        inputs = self.driver.find_elements(By.CSS_SELECTOR,"div[role='main'] input[type='text']")
        title = inputs[1]
        print('title')
        price = inputs[2]
        print('price')




        #定位控件2

        description = self.driver.find_elements(By.CSS_SELECTOR,"div[role='main'] textarea")[0]
        print('description')
        tags = self.driver.find_elements(By.CSS_SELECTOR,"div[role='main'] textarea[rows='1']")[0]

        City = self.driver.find_elements(By.CSS_SELECTOR,"div[role='main'] input[type='text'][aria-label='Location']")
        City = City[0]
        print('city')


        pyperclip.copy(titletxt)
        title.send_keys(Keys.CONTROL,"a")
        title.send_keys(Keys.CONTROL,"v")


        #title.send_keys(titletxt)
        price.send_keys(Keys.CONTROL,"a")
        price.send_keys(pricetxt)
        print('price update')
        
        pyperclip.copy(desctxt)
        description.send_keys(Keys.CONTROL,"a")
        description.send_keys(Keys.CONTROL,"v")
        print('desc update')
        
        pyperclip.copy(raw_tags)
        tags.send_keys(Keys.CONTROL,"v")
        tags.send_keys(Keys.ENTER)
        print('tags update')

        pyperclip.copy(location_str)
        City.send_keys(Keys.CONTROL,"a")
        City.send_keys(Keys.CONTROL,"v")
        # time.sleep(1)
        # cityoption = self.driver.find_elements(By.CSS_SELECTOR,"ul[role='listbox'][aria-label='5 suggested searches'] li[role='option']")[0]
        # cityoption.click()

        #update = self.driver.find_elements(By.CSS_SELECTOR,"div[role='button'][aria-label='Update']")[0]
        #update.click()

    def autoupdatelink(self):
        #进入编辑页面并读取城市名
        partern = r'([\w\s\'-]+),\s*(ON|QC|AB|NB)'
        Cityname = ''
        Provincename = ''
        city = self.driver.find_elements(By.CSS_SELECTOR,"span[dir='auto'] a span")
        for i in city:
            matches = re.findall(partern,i.text)
            if bool(matches):
                Cityname = matches[0][0].strip()
                Provincename = matches[0][1][0].strip()
                break
        
        location_str = Cityname+','+Provincename
        
        editlist = self.driver.find_elements(By.CSS_SELECTOR,"a[aria-label='Edit'][role='link'][href]")[0]
        editlist.click()

        element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div[role='main'] input[type='text'][aria-label='Location']")))

        titletxt = "Workbench"
        pricetxt = "1080"
        desctxt = "xxx:1080,xxxx:1050:xxxx1020"
        catetxt = "Tools"

        #文案读取
        with open(self.folderpath+'title.txt','r', encoding="utf-8") as titlef:
            titletxt = titlef.read()

        with open(self.folderpath+'price.txt','r') as pricef:
            pricetxt = pricef.read()

        with open(self.folderpath+'desc.txt','r', encoding="utf-8") as descf:
            desctxt = descf.read()
        
        with open(self.folderpath+'tags.txt','r', encoding="utf-8") as tagf:
            raw_tags = tagf.read()
        
        with open(self.folderpath+'cate.txt', 'r') as catef:
            catetxt = catef.read()
            catetxt.strip()


        #控件定位
        
        inputs = self.driver.find_elements(By.CSS_SELECTOR,"div[role='main'] input[type='text']")
        title = self.driver.find_element(By.CSS_SELECTOR,"div[role='main'] label[aria-label='Title'] input[type='text']")
        print('title')
        price = self.driver.find_element(By.CSS_SELECTOR,"div[role='main'] label[aria-label='Price'] input[type='text']")
        print('price')




        #定位控件2

        description = self.driver.find_element(By.CSS_SELECTOR,"div[role='main'] label[aria-label='Description'] textarea")
        print('description')
        tags = self.driver.find_element(By.CSS_SELECTOR,"div[role='main'] label[aria-label='Product tags'] textarea")

        City = self.driver.find_elements(By.CSS_SELECTOR,"div[role='main'] input[type='text'][aria-label='Location']")
        City = City[0]
        print('city')


        pyperclip.copy(titletxt)
        title.send_keys(Keys.CONTROL,"a")
        title.send_keys(Keys.CONTROL,"v")


        #title.send_keys(titletxt)
        price.send_keys(Keys.CONTROL,"a")
        price.send_keys(pricetxt)
        print('price update')
        
        pyperclip.copy(desctxt)
        description.send_keys(Keys.CONTROL,"a")
        description.send_keys(Keys.CONTROL,"v")
        print('desc update')
        
        pyperclip.copy(raw_tags)
        tags.send_keys(Keys.CONTROL,"v")
        tags.send_keys(Keys.ENTER)
        print('tags update')

        pyperclip.copy(location_str)
        City.send_keys(Keys.CONTROL,"a")
        City.send_keys(Keys.CONTROL,"v")
        # time.sleep(1)
        # cityoption = self.driver.find_elements(By.CSS_SELECTOR,"ul[role='listbox'][aria-label='5 suggested searches'] li[role='option']")[0]
        # cityoption.click()

        #update = self.driver.find_elements(By.CSS_SELECTOR,"div[role='button'][aria-label='Update']")[0]
        #update.click()



        
    def quit(self):
        #关闭浏览器
        self.status=0#浏览器状态设为关闭
        try:
            self.driver.execute('javascript:void(0);')
            self.driver.quit()
        except Exception as e:
            print(e)

