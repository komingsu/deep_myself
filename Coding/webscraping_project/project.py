# 날씨 가져오기
import requests
from bs4 import BeautifulSoup
import re
from time import time
from selenium import webdriver

time_check = time()
headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}

def create_soup(url):
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

def print_news(index, title, link):
    print("{}. {}".format(index+1, title))
    print("  (링크 : {})".format(link))

def scrape_weather():
    #날씨정보
    print("[오늘의 날씨]")
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%98%A4%EB%8A%98+%EB%B6%80%EC%82%B0+%ED%95%98%EB%8B%A8%EB%8F%99+%EB%82%A0%EC%94%A8"
    soup = create_soup(url)
    cast = soup.find("p", attrs={"class" : "summary"}).get_text()
    curr_temp = soup.find("div", attrs={"class" : "temperature_text"}).get_text().replace("현재 온도","")
    min_temp = soup.find("span", attrs={"class" : "lowest"}).get_text().replace("최저 기온","")
    max_temp = soup.find("span", attrs={"class": "highest"}).get_text().replace("최고 기온","")
    morning_rain_rate = soup.find_all("span", attrs={"class" : "rainfall"})[0].get_text()
    afternoon_rain_rate = soup.find_all("span", attrs={"class" : "rainfall"})[1].get_text()
    todat_list = soup.find_all("ul", attrs={"class" : "today_chart_list"})[0].get_text().replace("   ","")

    #출력
    print(cast)
    print("현재 {} (최저{} / 최고{})".format(curr_temp, min_temp, max_temp))
    print("오전 강수확률 {} / 오후 강수확률 {}".format(morning_rain_rate, afternoon_rain_rate))
    print(todat_list)
    print()
    #미세먼지 정보


def scrape_headline_news():
    print("[헤드라인 뉴스]")
    url = "https://news.naver.com"
    soup = create_soup(url)
    news_list = soup.find("ul", attrs= {"class" : "hdline_article_list"}).find_all("li", limit=5) #limits를 통해 가져오는 기사 갯수 설정가능
    for index, news in enumerate(news_list):
        title = news.find("a").get_text().strip()
        link = url + news.find("a")["href"]
        print_news(index, title, link)
    print()
        

def scrape_IT_news():
    print("[IT 뉴스]")
    url = "https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=105&sid2=230"
    soup = create_soup(url)
    news_list = soup.find("ul", attrs= {"class" : "type06_headline"}).find_all("li", limit=5) #limits를 통해 가져오는 기사 갯수 설정가능
    for index, news in enumerate(news_list):
        a_idx = 0
        img = news.find("img")
        if img:
            a_idx = 1 #img 태그가 있으면 1번째 a 태그의 정보를 사용
        a_tag = news.find_all("a")[a_idx]
        title = a_tag.get_text().strip()
        link = a_tag["href"]
        print_news(index, title, link)
    print()

def scrape_english():
    print("[오늘의 영어 회화]")
    url = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english&keywd=haceng_submain_lnb_eng_I_others_english&logger_kw=haceng_submain_lnb_eng_I_others_english"
    soup = create_soup(url)
    sentences = soup.find_all("div", attrs={"id": re.compile("^conv_kor_t")})
    print("(영어지문)")
    for sentence in sentences[len(sentences)//2 : ]:
        print(sentence.get_text().strip())
    print()
    print("(한글지문)")
    for sentence in sentences[ : len(sentences)//2]:
        print(sentence.get_text().strip())




if __name__ == "__main__":
    scrape_weather() # 오늘의 날씨 정보 가져오기
    scrape_headline_news() # 헤드라인 뉴스 정보 가져오기
    scrape_IT_news()
    scrape_english()
    print(round(time()-time_check, 2))