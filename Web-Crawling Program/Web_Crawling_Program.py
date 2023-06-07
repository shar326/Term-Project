from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import urllib.request
import time
import os
import ssl

class Images:
    
    __countFhishingType = 0
    all_FhishingTypes = []

    def __init__(self, givenFhishingType):
        self.__fhishingtype = givenFhishingType
        Images.__countFhishingType = Images.__countFhishingType + 1
        Images.all_FhishingTypes.append(self)

    def setFhishingType(self, givenFhishingType):
        self.__fhishingtype = givenFhishingType
    
    def getFhishingType(self):
        return self.__fhishingtype

    def __str__(self):
        msg = "{}".format(self.__fhishingtype)
        return msg
    
    def getNumOfFhishingType():
        return Images.__countFhishingType
    
# Fhishing1 = Images("스미싱")
Fhishing2 = Images("스피어 피싱")
# Fhishing3 = Images("피싱 사이트")
# Fhishing4 = Images("큐싱")

Fhishing_Type = Images.all_FhishingTypes

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(options=chrome_options)

def Image_Crawling():

    def createDirectory(directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print("Error: 폴더 생성에 실패했습니다.")

    driver.get('https://www.google.co.kr/imghp?hl=ko&ogbl')

    for image_name in Fhishing_Type:
        dir = ".\Image" + "\\" + str(image_name)
        createDirectory(dir)

        search = driver.find_element(By.ID,"APjFqb")
        search.clear()
        search.send_keys("{} 예시".format(str(image_name)))
        search.send_keys(Keys.RETURN)
        
        time.sleep(4)
        print('--- 스크롤 중 ---')
        elem = driver.find_element(By.TAG_NAME, "Body")
        for j in range(70):
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.1)
        image = driver.find_elements(By.CSS_SELECTOR,"img.rg_i.Q4LuWd")
        print(str(image_name)+" 이미지 개수 : ", len(image))
        link_list = []
        failure_count = 0
        count = 1
        for img in image:
            try:
                img.click()
                time.sleep(1)
                imgUrl = driver.find_element(By.XPATH,"//*[@id=\"Sva75c\"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]").get_attribute('src')
                link_list.append(imgUrl)
                print(str(image_name) + ' 링크 수집 중 ..... 진행 현황 : '+ str(count - failure_count)+ ' / ' + str(len(image)))
                count += 1
            except:
                print("Error occurred while collecting url")
                failure_count += 1
                continue

        ssl._create_default_https_context = ssl._create_unverified_context    
        for a,b in enumerate(link_list):
            try:
                url = b
                path = "C:\\Users\\shar\\OneDrive - 경희대학교\\문서\\WebPython Programing\\Term_Project\\Image\\{}".format(str(image_name))
                urllib.request.urlretrieve(url, "{}\\{}_{}.jpg".format(path, str(image_name), a+1))
                print("다운로드 성공!")
            except:
                print("Error occurred while downloading image")
                pass

        reset = driver.find_element(By.CLASS_NAME,"TYpZOd")
        reset.click()
        reset2 = driver.find_element(By.XPATH,"//*[@id=\"gb\"]/div/div[1]/div/div[2]/a")
        reset2.click()
    driver.close()

Image_Crawling()