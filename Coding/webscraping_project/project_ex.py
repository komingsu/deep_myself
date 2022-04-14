
import requests
from bs4 import BeautifulSoup

url = "https://news.naver.com"
res = requests.get(url)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")
news_list = soup.find("ul", attrs={"class" : "hdline_article_list"}).find_all("li")
print(news_list)