from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

def setChromeDoNotClose(boolean) :
    while boolean:
        pass

def getReviewToString(driver, xpath):
    try:
        return driver.find_element_by_xpath(xpath).text
    except NoSuchElementException:
        return "해당 항목 작성하지 않음."

def getReviewsToString(driver, xpath, ind):
    try:
        return driver.find_elements_by_xpath(xpath)[ind].text
    except IndexError:
        return "해당 항목 작성하지 않음."
    except NoSuchElementException:
        return "해당 항목 작성하지 않음."

def getReviewImagesUrl(driver, reviewdict, xpath='./div[@class="c_product_review_cont"]/div[@class="cont"]/div[@class="c_product_review_thumbnail2"]/ul/li'):
    try:
        img_links = []
        for img in driver.find_elements_by_xpath(xpath):
            img_links.append(
                img.find_element_by_xpath("./button").get_attribute("style").split('");')[0].split('url("')[1])
        reviewdict["img_links"] = img_links
    except NoSuchElementException:
        reviewdict["img_links"] = []
        pass

CHROME_URL = 'c:/chromedriver/chromedriver.exe'
URL = 'http://www.11st.co.kr/products/2752653725?trTypeCd=PW00&trCtgrNo=1001878'

#드라이버 셋팅
driver = webdriver.Chrome(CHROME_URL)
driver.implicitly_wait(3)
driver.get(URL)

#상품리뷰 버튼 눌러서 해당 위치로 이동
driver.find_element_by_xpath('//button[@id="tabMenuDetail2"]').click()

#리뷰가 들어가있는 iframe으로 이동
driver.switch_to.frame("ifrmReview")

reviewlist=[]
arealist=[]

#더보기 버튼 다 눌러 다...
while True:
    try:
        driver.find_element_by_xpath('//div[@id="review-list-page-area"]/div[@class="area_btn review-next-list-div"]/button').click()
        time.sleep(1.5)
    except NoSuchElementException:
        break

#리뷰 리스트 끌고 오기
arealist = driver.find_elements_by_xpath('//div[@id="review-list-page-area"]/ul[@class="area_list"]')


for i in arealist:
    liList = i.find_elements_by_css_selector('li')
    for ind, j in enumerate(liList):
        #리뷰 리스트가 아니라 다른 리스트를 가져올 경우 다음거로
        try:
            j.find_element_by_xpath('./dl[@class="c_product_reviewer"]')
        except NoSuchElementException:
            continue

        reviewdict = {}
        reviewdict["name"] = getReviewToString(j, './dl[@class="c_product_reviewer"]/dt[@class="name"]')
        reviewdict["grade"] = getReviewToString(j, './div[@class="c_product_review_cont"]/p[@class="grade"]/span[@*]/em')
        reviewdict["option"] = getReviewToString(j, './div[@class="c_product_review_cont"]/p[@class="option"]')
        reviewdict["speed"] = getReviewsToString(j, './div[@class="c_product_review_cont"]/div[@class="cont"]/div[@class="value"]/dl/dd', 0)
        reviewdict["size"] = getReviewsToString(j, './div[@class="c_product_review_cont"]/div[@class="cont"]/div[@class="value"]/dl/dd', 1)
        reviewdict["fine"] = getReviewsToString(j, './div[@class="c_product_review_cont"]/div[@class="cont"]/div[@class="value"]/dl/dd', 2)
        reviewdict["content"] = getReviewToString(j, './div[@class="c_product_review_cont"]/div[@class="cont"]/div[@class="cont_text_wrap"]/p[@class="cont_text"]')
        reviewdict["date"] = getReviewToString(j, './div[@class="c_product_review_cont"]/p[@class="side"]/span[@class="date"]')
        #이미지 있는지 없는지 확인하고 있으면 url만 가져오기.
        getReviewImagesUrl(j, reviewdict)

        reviewlist.append(reviewdict)
        print(reviewdict)

print("읽어드린 리뷰의 개수 : {0}".format(len(reviewlist)))
setChromeDoNotClose(True)
