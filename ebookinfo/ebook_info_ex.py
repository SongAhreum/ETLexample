import os
import datetime
import requests
import json
import csv

class ebook_list():
    
    def __init__(self) : 
        #파라미터로 params에 들어갈 value값 지정하면 원하는 범위만큼 data수집가능?/ but 전체data가져올거임
        self.path =  'iris서버에서,cvs파일저장할폴더위치'#home/iris/user/song/data
        
    
    #수집날짜를을 파일명칭으로 directory생성    
    def makedir(self,path):
        now = datetime.datetime.now()
        dir_name = now.strftime('%Y.%m.%d') #날짜별 수집예정
        full_path = os.path.join(path, dir_name)
        
        #directory 존재 시
        if os.path.exists(full_path):
            return

        os.makedirs(full_path)
        return full_path, dir_name
    
    def collect(self) : 
        
        full_path, dir_name = self.makedirs(self.path)
        
        pageNo = 0
        columns = []
        while 1 :
            pageNo += 1
            numOfRows = 1000
            self.url = 'https://apis.data.go.kr/4050000/libebook/getLibebook?serviceKey=4qZmheMC8zC45UjTqUJ37kWIGPr4KjCyz9co0PFLk17dUNa%2BZc4Uv7xGBugqrBOu6xfwVTNXlnm3otyEEeGrMg%3D%3D&pageNo={pageNo}&numOfRows={numOfRows}'
            self.response = requests.get(self.url)
            
            #response status확인 하려고했으나 reusltCode의 value값이 0인경우로 하는게...?
            #if self.response.status_code == 200:  
            
            #json parsing
            parsed_body = json.loads(self.response.text)
            #전체data갯수
            totalCount = int(parsed_body.get('totalCount'))
            resultCode = int(parsed_body.get('resultCode'))
            #페이지당 last_no = parsed_body_ex['items'][-1]['no']
            #if int(last_no)-1 == totalCount : break
            
            if resultCode == 0 : 
                # resultCode 0은 성공, 3은 noData ,11은 parameterError
                # status_code가 500인데도 받아야할 data가 있을때도 있음
                # 수집 할 data도 없고 resultCode도 없는경우? 예외처리로 잡아야하나?
                
                
                #column = ['no','gnr','ebk_nm','aut_nm','pblshr','pblsh_ymd','loan_avlbl_yn','rsvt_noppl','avlbl_envrmt','cn_intro','srvc_form']
                if not columns :
                    columns = list(parsed_body['items'][0].keys()) 
                
                #csv파일 저장
                with open(dir_name,'a',newline='') as f:
                    csvfile = csv.writer(f,delimiter=',',quotechar='"',escapechar='\\', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
                    #csv파일 columns 기록
                    csvfile.writerow(['#'+columns[0]]+columns[1:])
                    for item in parsed_body['items']: #item변수에 담기는건 dictionary
                        csvfile.writerow(item)
            else : break            

def main() :
    obj = ebook_list()
    obj.makedir(obj.path) ###path를 모르겠음~ #home/iris/user/song/?datairis>user>song>EBOOK>data>날짜별로 directory생성할?
    obj.collect()
    
if __name__ == '__main__' :
	main()
	