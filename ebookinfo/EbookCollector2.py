import os
import sys
import datetime
import requests
import json
import csv

'''while문 조건을 수집시점으로
  conf파일?configparser모듈필요
'''
class ebook_list():
    
    def __init__(self) : 
      #저장경로
      self.path = 'C:\\Users\\82108\\Desktop\\ETLexample\\ebook_csv'
    
    def collect(self) :  
      now = datetime.datetime.now()
      filename = 'ebook_' + now.strftime('%Y.%m.%d') #날짜별 수집예정   
      csv_path = os.path.join(self.path,filename)
      columns = []
      pageNo = 0
      numOfRows = 1000
      #totalCount 미리 받을까 했는데 한번수집갯수 1000개라 임의로 지정, response결과에서 값받아서 초기화
      totalCount = 1000 
      
      #pageNo=12까지 수집되어야함
      while (pageNo * numOfRows) < totalCount:
        pageNo += 1
        
        #url로 data가져오기(json)
        #f-stirng  .format() 차이?        
        url = 'https://apis.data.go.kr/4050000/libebook/getLibebook?serviceKey=4qZmheMC8zC45UjTqUJ37kWIGPr4KjCyz9co0PFLk17dUNa%2BZc4Uv7xGBugqrBOu6xfwVTNXlnm3otyEEeGrMg%3D%3D&pageNo={}&numOfRows={}'.format(pageNo,numOfRows) 
        response = requests.get(url)
        
        #json parsing
        parsed_body = json.loads(response.text)
        #응답결과코드(데이터 스펙 확인해 볼 것)      
        resultCode = int(parsed_body.get('resultCode'))
        #전체 데이터수 세팅
        totalCount = int(parsed_body.get('totalCount'))
        
        if response.status_code == 200:
          if resultCode == 0 :
            
            with open(csv_path,'a') as f:
              csvfile = csv.writer(f,delimiter=',',quotechar='"',escapechar='\\', quoting=csv.QUOTE_MINIMAL, lineterminator='\n',encoding='utf-8')
              #csv파일 columns 기록
              if not columns :
                columns = list(parsed_body['items'][0].keys()) 
                csvfile.writerow(['#'+columns[0]]+columns[1:])
              for item in parsed_body['items']: #item변수에 담기는건 dictionary
                csvfile.writerow(item.values()) #writerow는 list만?
          else : return # resultcode 에러일때 출력?    
        else : return    #status_code에러일때 출력
def main() :
  obj = ebook_list()
  obj.collect()
  #stdout으로 csv_path전달
    
if __name__ == '__main__' :
	main()          
