# 동적 페이지 스크랩
import requests
from bs4 import BeautifulSoup
headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36", "Accept-Language" : "ko-KR,ko"}

url = "https://play.google.com/store/movies/top"
res = requests.get(url, headers= headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")

movies = soup.find_all("div", attrs= {"class" : "ImZGtf mpg5gc"})
print(len(movies))

#html 정보를 싹 가져옴
#with open("movie.html", "w", encoding="utf8") as f:
#    #f.write(res.text)
#    f.write(soup.prettify()) #html 문서를 예쁘게 가져옴

for movie in movies:
    title = movie.find("div", attrs={"class":"WsMG1c nnK0zc"}).get_text()
    print(title)