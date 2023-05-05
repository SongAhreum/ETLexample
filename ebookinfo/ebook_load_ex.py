#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import traceback
import json
import time
import datetime
import csv
import configparser
import pymysql


class EbookLoader():
  def __init__(self) :

    self.ehost = '127.0.0.1'
    self.eid = 'root'
    self.epawd = 'root'
    self.eport = 3306
    self.edbnm = 'etl_example'
    self.echset = 'utf8'
    self.ewait = 10
    #timeout은 초단위여함->int 
    #테이블명 : tb_ebooksample
    self.csv_path =os.path.join('C:\\Users\\82108\\Desktop\\ETLexample\\ebook_csv','ebook_2023.04.30')
    #stdin으로 csv_path받을거임
    #2개의 값으로 받을경우 json으로 날리고 json으로받아 pasing
    # ex) data = json.loads(sys.stdin.readline().strip())
    # self.csv_path = data[0]
    # self.columns = data[1]
    
  def truncateTable(self,conn) :
    cursor = conn.cursor()
    turncate_query = 'TURNCATE TABLE tb_ebooksample'
    cursor.execute(turncate_query)
    conn.commit() 
    
  
  def DBConnect(self):
    # conn = mysql.connector.connect(host=self.ehost, port=self.eport, user=self.eid, password=self.epawd, database=self.edbnm, timeout = self.ewait) 
    try:
      conn = pymysql.connect(host=self.ehost, port=self.eport, user=self.eid, password=self.epawd, database=self.edbnm, charset=self.echset) 
      print('db연결성공')
    except: print('db연결실패')
    
    return conn
  
  def load(self):
    #db연결
    conn = self.DBConnect()
    #중복방지 테이블삭제
    self.truncateTable(conn)
    
    #csv파일읽기
    with open(self.csv_path) as csvfile:
      reader = csv.reader(csvfile, delimiter=',', quotechar='"', escapechar='\\', quoting=csv.QUOTE_MINIMAL, lineterminator='\n',encoding='utf-8')
      
      #SQL만들기
      #물음표는 SQL prepared statement에서 매개변수를 나타내는 placeholder로 사용
      #data로들어가는 튜플의 요소와 values요소와 매핑되기때문에 갯수맞아야함
      insert_query = "INSERT INTO tb_ebooksample (GNR, EBK_NM, AUT_NM, PBLSHR, PBLSHR_YMD, LOAN_AVLBL_YN, RSVT_NOPPL, AVLBL_ENVMT, CN_INTRO, SRVC_FORM) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
      
      rows = []
      for row in reader:
        data = [row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10]]
        rows.append(tuple(data))
        #rows에 한번data가추가될때마다 한행씩들어가는것(한행은 튜플)    
    cursor = conn.cursor()
    cursor.executemany(insert_query,rows)
    #execute와 executemany차이점 정리하기
    conn.commit() 
    conn.close()



  def run(self):
    #load함수의 기능을고려해서도, load함수에  db connection기능과 truncate기능을하는 함수를 포함하는 것이 좀더 객체지향적임 
    self.load()



def main() :
  obj = EbookLoader()
  obj.run()
  
if  __name__ == "__main__" :
  main()