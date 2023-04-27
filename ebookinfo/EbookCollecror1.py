dimport os
import sys
import datetime
import requests
import json
import csv
 

class ebook_list():
    
    def __init__(self) : 
        #파라미터로 params에 들어갈 value값 지정하면 원하는 범위만큼 data수집가능?/ but 전체data가져올거임
      self.path = '/home/iris/user/song/EBOOK/data'
    
    def collect(self) :  
      now = datetime.datetime.now()
      filename = 'ebook_'+now.strftime('%Y.%m.%d') #날짜별 수집예정   
      csv_path = os.path.join(self.path,filename)
      columns = []
      pageNo = 0
      
      while 1:
       
        pageNo += 1
        numOfRows = 1000
        #while문 밖에?가능?numOfRows 
              
        
        
        self.url = 'https://apis.data.go.kr/4050000/libebook/getLibebook?serviceKey=4qZmheMC8zC45UjTqUJ37kWIGPr4KjCyz9co0PFLk17dUNa%2BZc4Uv7xGBugqrBOu6xfwVTNXlnm3otyEEeGrMg%3D%3D&pageNo={}&numOfRows={}'.format(pageNo,numOfRows) 
        #format?f stri:ng?
        
        self.response = requests.get(self.url)
        #json parsing
        parsed_body = json.loads(self.response.text)
        
        #TypeError: int() argument must be a string, a bytes-like object or a number, not 'NoneType' 때문에 if절사용
        #전체data갯수ex)11840
        if (parsed_body.get('totalCount')) is not None:
          totalCount = int(parsed_body.get('totalCount'))
        if (parsed_body.get('resultCode')) is not None:
          resultCode = int(parsed_body.get('resultCode'))
        
        #전체데이터갯수 넘어갈때 break
        if (pageNo-1) * numOfRows > totalCount:
          break
        
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
 
'''
pageNo = 0
while 1:
        pageNo += 1
        numOfRows = 1000
        
        self.url = 'https://apis.data.go.kr/4050000/libebook/getLibebook?serviceKey=4qZmheMC8zC45UjTqUJ37kWIGPr4KjCyz9co0PFLk17dUNa%2BZc4Uv7xGBugqrBOu6xfwVTNXlnm3otyEEeGrMg%3D%3D&pageNo={}&numOfRows={}'.format(pageNo,numOfRows)
#이 형태로 시작하기때문에 totalCount의 값을 받을 시기와
# if (pageNo-1) * numOfRows > totalCount:
          break        
  를 넣을 시기가 애매했음 
  
#while문 밖에서 totalCount값을 받고 시작했어야 했나?        
'''         