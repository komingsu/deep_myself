#정해진 형태의 식 reqular experation
#ex) 주민등록번
#901201-1111111  (o)
#abcdef-1111111  (X)
#이메일 주소
#nadocoding@gmail.com
#차량번호
#11가 1234, 123가 1234
#IP 주소
#192.168.0.1

import re

#p=패턴, 
# . : 은 하나의 문자를 의미 (ca.e) (care, cafe, case)
# ^ : 문자열의 시작을 의미 (^de) (desk, destination)
# $ : 문자열의 끝 (se$) (case, base)



p = re.compile("ca.e")
#print(m.group()) #매치되지 않으면 에러가 발생 - group 함수



def print_match(m):
    if m:
        print("m.group():", m.group()) #일치하는 문자열 반환
        print("m.string():", m.string) # 입력받은 문자열
        print("m.start():", m.start()) #일치하는 문자열의 시작
        print("m.end::", m.end()) # 일치하는 문자열의 끝
        print("m.span():", m.span()) #일치하는 문자열의 시작
    else:
        print("매칭 x")


m = p.match("careless") # 주어진 문자열의 처음부터 일치하는지 확인 -> 뒤부터는 보지 않음
print_match(m)

m = p.search("good care") # search : 주어진 문자열중에 일치하는게 있는지 확인
print_match(m)

m = p.search("careless")
print_match(m)

lst = p.findall("good care cafe") #findall : 일치하는 모든것을 리스트로 반환
print(lst)

# 1. p = re.comfile("원하는 형태")
# 2. m = p.match("비교할 문자열") : 주어진 문자열의 처음부터 일치하는지 확인
# 3. m = p.search("비교할 문자열") : 주어진 문자열 중에 일치하는게 있는지 확인
# 4. lst = p.findall("비교할 문자열:") : 일치하는 모든것을 "리스트" 형태로 반환

#정규직의 추가공부는 w3schools 에서 Python >> RegEx
# Python re >> 파이썬 정규 dox 에서 확인가능