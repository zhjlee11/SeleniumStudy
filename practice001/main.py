from selenium import webdriver

driver = webdriver.Chrome('c:/chromedriver/chromedriver.exe')
driver.implicitly_wait(3)
driver.get('https://nid.naver.com/nidlogin.login')
driver.find_element_by_name('id').send_keys('laplace2004')
driver.find_element_by_name('pw').send_keys('2004STEVE*')
# 로그인 버튼을 눌러주자.
driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
