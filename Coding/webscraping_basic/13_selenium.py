from selenium import webdriver
from selenium.webdriver.common.keys import Keys #ENTER 하기 위해서 필요한 기능
import time

browser = webdriver.Chrome("./chromedriver.exe")



#로그인 버튼 클릭
#elem = browser.find_element_by_class_name("link_login")
#elem.click()

#browser.back() 
#browser.forward()
#browser.refresh()
#browser.close() 탭 닫기
#browser.quit() 전체닫기

# 1. 네이버 이동
browser.get("http://naver.com") #다음 주소로 바로 이동

# 2. 로그인 버튼 클릭
elem = browser.find_element_by_class_name("link_login")
elem.click()

# 3. 아이디 패스워드 입력

browser.find_element_by_id("id").send_keys("naver_id")
time.sleep(2)
browser.find_element_by_id("pw").send_keys("password")

# 4. 로그인 버튼 클릭
browser.find_element_by_id("log.login").click()

time.sleep(3)

# 5. 아이디 새로 입력

browser.find_element_by_id("id").clear() #그 자리에 있는 값을 지워줌
browser.find_element_by_id("id").send_keys("my_id")

# 6. html 정보 출력

print(browser.page_source) #현재 페이지의 모든 정보를 출력

# 7. 브라우저 종료

browser.quit()