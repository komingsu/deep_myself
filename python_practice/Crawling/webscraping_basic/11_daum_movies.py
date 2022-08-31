import requests
from bs4 import BeautifulSoup


for year in range(2015, 2020): #2015년 부터 2020년까지 다 훑기
    url = "https://search.daum.net/search?w=tot&q={}%EB%85%84%EC%98%81%ED%99%94%EC%88%9C%EC%9C%84&DA=MOR&rtmaxcoll=MOR". format(year)
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    images =soup.find_all("img", attrs={"class" : "thumb_img"})

    for idx, image in enumerate(images):
        #print(image["src"])
        image_url = image["src"]
        if image_url.startswith("//"):
            image_url = "https:" + image_url

        print(image_url)

        image_res = requests.get(image_url)
        image_res.raise_for_status()

        with open("movie_{}_{}.jpg".format(year, idx+1), "wb") as f: #년도를 구분해주기위해 {}를 2개 사용
            f.write(image_res.content) #여기서 content가 이미지 이다
        
        if idx >= 4:  #상위 5개 이미지까지만 다운로드
            break