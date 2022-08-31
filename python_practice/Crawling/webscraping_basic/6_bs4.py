import requests
from bs4 import BeautifulSoup

url = "https://comic.naver.com/webtoon/weekday"
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")
print(soup.title)
print(soup.a) #처음으로 발견되는 a 엘리먼트
print(soup.a.attrs)
#{'href': '#menu', 'onclick': "document.getElementById('menu').tabIndex=-1;document.getElementById('menu').focus();return false;"}
#위와 같이 딕셔너리 형태로 가져옴
print(soup.a["href"])
##menu 를 가져오는것을 볼 수 있음

print(soup.find("a", attrs={"class":"Nbtn_upload"})) # class = "Nbtn_upload" 인 a element 를 찾아줘
print(soup.find(attrs={"class":"Nbtn_upload"})) #class = "Nbtn_upload" 인 어떤 element 를 찾아줘
rank1 = soup.find("li", attrs={"class": "rank01"}) # rank01 의 값을가져옴
print(rank1.a)

#형제 element 를 가져오기

print(rank1.a.get_text())
print(rank1.next_sibling) #1번 next_sibling 을 했음에도 안나오는 경우가 있음 그건 공백이 있을때 안나옴
print(rank1.next_sibling.next_sibling)

rank2 = rank1.next_sibling.next_sibling
rank3 = rank2.next_sibling.next_sibling
print("                       ")

print(rank3.a.get_text)
print(rank1.parent)
rank2 = rank1.find_next_sibling("li")

print(rank2.a.get_text)

webtoon = soup.find("a", text="독립일기-시즌2 8화 반려견 운동장")
print("                       ")
print("                       ")
print(webtoon)
