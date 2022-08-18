import re
import requests
from bs4 import BeautifulSoup

url = "https://www.coupang.com/np/search?q=%EB%85%B8%ED%8A%B8%EB%B6%81&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page=1&rocketAll=false&searchIndexingToken=1=6&backgroundColor="
headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}
res = requests.get(url, headers = headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")

#print(res.text)

items = soup.find_all("li", attrs={"class" : re.compile("^search-product")})
print(items[0].find("div", attrs={"class" : "name"}).get_text())

for item in items :

    #광고제품 제외하기
    ad_badge = item.find("span", attrs={"class":"ad-badge-text"})
    if ad_badge:
        print("<광고 상품 제외합니다>")
        continue
    name = item.find("div", attrs={"class" : "name"}).get_text()

    #애플 제품 제외하기
    if "Apple" in name:
        print(" <Apple 상품 제외합니다>")
        continue

    price = item.find("strong", attrs={"class" : "price-value"}).get_text() #가격

    #리뷰 100개 이상, 평점 4.5 이상 되는 것만 조회하기

    #평점이 없는것, 평점 수가 없는것 제외
    rate = item.find("em", attrs={"class" : "rating"})
    if rate:
        rate = rate.get_text()
    else:
        print(" <평점 없는 상품 제외합니다>")
        continue
    rate_count = item.find("span", attrs={"class" : "rating-total-count"}) #평점갯수
    if rate:
        rate_count = rate_count.get_text()
        rate_count = rate_count[1:-1]
    else:
        print("<평점 수 없는 상품 제외합니다>")
        continue

    # 평점이 4.5 보다 크고 평가 갯수가 50개 이상이면 print
    if float(rate) >= 4.5 and int(rate_count) >= 100:
        print(name, price, rate, rate_count)

