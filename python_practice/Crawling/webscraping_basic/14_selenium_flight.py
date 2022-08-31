from selenium import webdriver

# selenium 으로 검색중 로딩 처리하기 툴
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
browser.maximize_window() #창 최대화

url = "https://beta-flight.naver.com/"
browser.get(url)

# 가는 날 선택
browser.find_element_by_xpath("//*[@id='__next']/div/div[1]/div[4]/div/div/div[2]/div[2]/button[1]").click()

# 이번달 27, 다음달 28일 선택
browser.find_element_by_xpath("//*[@id='__next']/div/div[1]/div[10]/div[2]/div[1]/div[2]/div/div[2]/table/tbody/tr[5]/td[4]/button").click()

# 검색중 로딩 처리 1) 몇초 기다리기. 2)elem 가 나올때까지 기다리기.

try:
    elem = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='__next']/div/div[1]/div[10]/div[2]/div[1]/div[2]/div/div[2]/table/tbody/tr[5]/td[4]/button"))) # 속성값이 나올때 까지 기다려라
    #성공했을 때 동작 수행 작성
finally:
    browser.quit # 실패시 브라우저 아웃