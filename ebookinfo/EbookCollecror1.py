import os
import sys
import datetime
import requests
import json
import csv

'''while무한루프에서 if절로 break'''
class ebook_list():
    
    def __init__(self) : 
        #파라미터로 params에 들어갈 value값 지정하면 원하는 범위만큼 data수집가능?/ but 전체data가져올거임
      self.path = 'C:\\Users\\82108\\Desktop\\ETLexample\\ebook_csv'
    
    def collect(self) :  
      now = datetime.datetime.now()
      filename = 'ebook_'+now.strftime('%Y.%m.%d') #날짜별 수집예정   
      self.csv_path = os.path.join(self.path,filename) #full path
      columns = []
      pageNo = 0
      
      while 1:
        pageNo += 1
        numOfRows = 1000  
        
        url = 'https://apis.data.go.kr/4050000/libebook/getLibebook?serviceKey=4qZmheMC8zC45UjTqUJ37kWIGPr4KjCyz9co0PFLk17dUNa%2BZc4Uv7xGBugqrBOu6xfwVTNXlnm3otyEEeGrMg%3D%3D&pageNo={}&numOfRows={}'.format(pageNo,numOfRows) 
        #format?f stri:ng?
        response = requests.get(url)
        #json parsing
        parsed_body = json.loads(response.text)
        
        if (parsed_body.get('totalCount')) is not None:
          totalCount = int(parsed_body.get('totalCount'))
        if (parsed_body.get('resultCode')) is not None:
          resultCode = int(parsed_body.get('resultCode'))
        
        #수집멈추는 시점  
        if (pageNo-1) * numOfRows > totalCount:
          break
        
        if response.status_code == 200:
          if resultCode == 0 :
            with open(self.csv_path,'a',encoding='utf-8') as f:
              csvfile = csv.writer(f,delimiter=',',quotechar='"',escapechar='\\', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
              #csv파일맨위 한줄 컬럼리스트
              if not columns :
                columns = list(parsed_body['items'][0].keys()) 
                csvfile.writerow(['#'+columns[0]]+columns[1:])
              #data수집  
              for item in parsed_body['items']: #item변수에 담기는건 dictionary
                csvfile.writerow(item.values()) #writerow는 list만?
          else: return # resultcode 에러일때     
        else : return # status_code 에러일때     
def main() :
  obj = ebook_list()
  obj.collect()
  #try catch문으로 -> stdout stderr사용
    
if __name__ == '__main__' :
	main()          

