from selenium import webdriver

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")

#이 아래부분을 적어줘야 headless chrome 이란것을 숨길 수 있다.
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36")

browser = webdriver.Chrome(options=options)
browser.maximize_window()

url = "https://www.whatismybrowser.com/detect/what-is-my-user-agent"
browser.get(url)

detected_value = browser.find_element_by_id("detected_value")
print("--------------------")
print(detected_value.text) # 속성안의 text 값 가져오기
print("--------------------")
browser.quit()

# selenium with python 을 통해 주가 공부를 할 수 있다.

# html 을 전체적으로 볼때는
# with open(" ", "w", encoding="utf8") as f:
#       f.write(soup.prottify())
# 를 통해 보면 좋다.