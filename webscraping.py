import os
import sys
os.chdir(sys.path[0])

import urllib.request, json 
import csv
import requests
import pandas as pd 
import googlemaps
import numpy as np

class Getdata:
    def __init__(self, source = 'https://data.taipei/opendata/datalist/apiAccess?scope=resourceAquire&rid=',
                    url_csv = sys.path[0] + '/database/url.csv',
                    data = sys.path[0] + '/database/1999_data.csv'):
        self.source = source
        self.url_csv = url_csv
        self.data = data

    ### 建立 url.csv 回傳 url list
    def __webscraping(self, method):
        with urllib.request.urlopen(self.source) as url:
            data = json.loads(url.read())
        CSV_URL = []
        for i in range(len(data["result"]["results"][0]["resources"])):
            CSV_URL.append(self.source + str(data["result"]["results"][0]["resources"][i]["resourceId"])+ "&format=csv")
        if method == True:
            CSV_URL = pd.DataFrame(CSV_URL)
            CSV_URL.to_csv(self.url_csv, mode='a',index = 0, header = 0)
            return CSV_URL
        else:
            return CSV_URL

    ### 地址轉經緯度
    def logchanger(self, csv_file, API_KEY):
        gm = googlemaps.Client(key = API_KEY)
        address_not_str = []
        df = csv_file
        if type(df) != str:
            for i in range(len(df)):
                if type(df["案件地址"][i]) != str:
                    address_not_str.append(i)
            location = []
            for i in range(len(df)):
                if i not in address_not_str:
                    try:
                        geocode_result = gm.geocode(df["案件地址"][i])[0]
                        location.append(geocode_result["geometry"]["location"])
                    except:
                        location.append(None)
                else:
                    location.append(None)
        else:
            location = gm.geocode(df)[0]["geometry"]["location"]
        return location

    ### Output 1999_data
    def __getdata(self, url_to_update, storage = True):
        url_list_from_webscraping = url_to_update
        my_list_ordered = []
        with requests.Session() as s:
            for i in url_list_from_webscraping:
                download = s.get(i)
                decoded_content = download.content.decode('utf-8')
                cr = csv.reader(decoded_content.splitlines(), delimiter=',')
                my_list = list(cr)	
                if len(my_list) == 0:
                    continue
                else:
                    if '派工項目' in my_list[0]:
                        index_time = my_list[0].index("立案時間")
                        index_project = my_list[0].index("派工項目")
                        index_address = my_list[0].index("案件地址")
                        for x in range(1,len(my_list)):
                            my_list_ordered.append([my_list[x][index_time],my_list[x][index_project],my_list[x][index_address]])			
                    else:
                        continue  
        if storage == True:
            list_from_get_data = pd.DataFrame(my_list_ordered)
            location = self.log_changer(list_from_get_data)
            list_from_get_data['經緯度'] = location
            list_from_get_data.columns = ["立案時間", "派工項目", "案件地址", "經緯度"]
            # 如果原先已經有1999_data
            if os.path.isfile(self.data):
                old = pd.read_csv(self.data)
                list_from_get_data = pd.concat([old, list_from_get_data])
                list_from_get_data.to_csv(self.data, index = False, header = None, encoding = 'cp950')
            # 沒有1999_data
            else:
                list_from_get_data.to_csv(self.data, index = False, header = None, encoding = 'cp950')
            return None
        else:
            return my_list_ordered

    def check_database(self):
        # 存在url
        if os.path.isfile(self.url_csv) and os.path.isfile(self.data):
            old_url_list = pd.read_csv(self.url_csv, encoding = 'cp950')
            old_url_list = list(old_url_list.iloc[1:,:])
            new_url_list = list(self.__webscraping(method = False))
            if len(new_url_list) != len(old_url_list):
                # 有需要更新的
                list_to_update = list(set(new_url_list) - set(old_url_list))
                print('更新資料庫請稍後...')
                self.__getdata(url_csv = list_to_update)
                return list_to_update
            else: 
                # 不需要更新
                list_to_update = False
                return None
        #  不存在url 或 不存在data.csv
        else:
            url_csv = self.__webscraping(method = True)
            self.__getdata(url_csv = list(url_csv.iloc[:,0]))
        return None

#### 使用指南 : Initialize的時候 call check_database
# g = Getdata()
# g.check_database()
