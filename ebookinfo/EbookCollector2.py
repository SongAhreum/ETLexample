import os
import sys
import datetime
import requests
import json
import csv

''' 요청변수
| 항목명(국문) | 항목명(영문) |
| --- | --- |
| 결과코드 | resultCode |
| 결과메시지 | resultMsg |
| 한 페이지 결과 수 | numOfRows |           ###필!
| 페이지 수 | pageNo |                      ###필!
| 데이터 총 개수 | totalCount |
| 번호 | no |                               ###필!
| 장르 | gnr |
| 전자도서명 | ebk_nm |
| 저자명 | aut_nm |
| 출판사 | pblshr |
| 출간일자 | pblsh_ymd |
| 대출가능여부 | loan_avlbl_yn |
| 예약인원 | rsvt_noppl |
| 이용 가능 환경 | avlbl_envrmt |
| 콘텐츠 소개 | cn_intro |
| 서비스 형태 | srvc_form |

    출력결과
| 항목명(국문) | 항목명(영문) |
| --- | --- |
| 결과코드 | resultCode |
| 결과메시지 | resultMsg |
| 한 페이지 결과 수 | numOfRows |
| 페이지 수 | pageNo |
| 데이터 총 개수 | totalCount |
| 번호 | no |
| 장르 | gnr |
| 전자도서명 | ebk_nm |
| 저자명 | aut_nm |
| 출판사 | pblshr |
| 출간일자 | pblsh_ymd |
| 대출가능여부 | loan_avlbl_yn |
| 예약인원 | rsvt_noppl |
| 이용 가능 환경 | avlbl_envrmt |
| 콘텐츠 소개 | cn_intro |
| 서비스 형태 | srvc_form |
'''
class ebook_list():
    
    def __init__(self) : 
      #저장경로
      self.path = '/home/iris/user/song/EBOOK/data'
      #data총량 ex)11840
      url_ex = 'https://apis.data.go.kr/4050000/libebook/getLibebook?serviceKey=4qZmheMC8zC45UjTqUJ37kWIGPr4KjCyz9co0PFLk17dUNa%2BZc4Uv7xGBugqrBOu6xfwVTNXlnm3otyEEeGrMg%3D%3D&pageNo=1&numOfRows=1'
      response_ex = requests.get(url_ex)
      parsed_body_ex = json.loads(response_ex.text)
      self.totalCount = int(parsed_body_ex.get('totalCount'))
    
    def collect(self) :  
      now = datetime.datetime.now()
      filename = 'ebook_'+now.strftime('%Y.%m.%d') #날짜별 수집예정   
      csv_path = os.path.join(self.path,filename)
      columns = []
      pageNo = 0
      numOfRows = 1000
      
      #pageNo=12까지 수집되어야함
      while (pageNo * numOfRows) < self.totalCount:
        pageNo += 1
        
        #url로 data가져오기(json)        
        self.url = 'https://apis.data.go.kr/4050000/libebook/getLibebook?serviceKey=4qZmheMC8zC45UjTqUJ37kWIGPr4KjCyz9co0PFLk17dUNa%2BZc4Uv7xGBugqrBOu6xfwVTNXlnm3otyEEeGrMg%3D%3D&pageNo={}&numOfRows={}'.format(pageNo,numOfRows) 
        self.response = requests.get(self.url)
        
        #json parsing
        parsed_body = json.loads(self.response.text)
        #응답결과코드      
        resultCode = int(parsed_body.get('resultCode'))
        
        # noData:3 / parameterError:11 / 성공:0 (status_code = 500일 경우도있음(마지막 data page) )
        if resultCode == 0 :
          if not columns :
            columns = list(parsed_body['items'][0].keys()) 
          with open(csv_path,'a',newline='') as f:
            csvfile = csv.writer(f,delimiter=',',quotechar='"',escapechar='\\', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            #csv파일 columns 기록
            csvfile.writerow(['#'+columns[0]]+columns[1:])
            for item in parsed_body['items']: #item변수에 담기는건 dictionary
              csvfile.writerow(item.values()) #writerow는 list만?
        else : return      
def main() :
  obj = ebook_list()
  obj.collect()
    
if __name__ == '__main__' :
	main()          
 
