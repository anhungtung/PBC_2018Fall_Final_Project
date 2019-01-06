import os
import sys
os.chdir(sys.path[0])

import numpy as np
import pandas as pd
import math
from webscraping import Getdata

class Backend:
    def __init__(self, data = sys.path[0] + '/database/1999_data.csv',
    fixed = sys.path[0] + '/database/address_list.csv'):
        self.data = data
        self.fixed = fixed
        self.fixedSet = None

    def __calculatedistance(self, user, target):
        la1, long1 = user[0], user[1]
        la2, long2 = target[1], target[0]
        lat = 110751.075273
        logi = 101751.561277
        d = ((abs(la1 - la2) * lat)**2 + (abs(long1 - long2) * logi)**2)
        return d
    
    def __checkfixed(self, address):
        if self.fixedSet == None:
            fixed = pd.read_csv(self.fixed, encoding = 'utf8')
            self.fixedSet = set(fixed.iloc[:,0])
        address = address[3:]
        if address in self.fixedSet:
            return True
        else:
            return False

    def dataupdate(self):
        table = pd.read_csv(self.data, encoding = 'utf8') #先指定第一行為indexcolumn
        table = table.rename(columns={'0':'經緯度'})
        table = table.drop(columns = ['laitude'], errors = 'ignore')
        table["longitude"] = np.nan
        table["latitude"] = np.nan
        table["longitude"] = table['經緯度'].str.split(",").str.get(0).str.lstrip( "(" )
        table["latitude"] = table['經緯度'].str.split(",").str.get(1).str.rstrip( ")" )
        table = table.to_csv(self.data, encoding = 'utf8', index = None)
        return None
  
    def __search(self, address, API_KEY, radius=500):
        table = pd.read_csv(self.data, encoding = 'utf8')
        #address -> coordinate
        coordinate = Getdata().logchanger(address, API_KEY)
        #calculate the distance and delete the coordinate that distance is larger than 'radius' and format to dictionary
        result = []
        dist = 0
        time = 0
        for i in range(table.shape[0]):
            if table['立案時間'][i] == float('NaN'):
                continue
            d = self.__calculatedistance([coordinate['lat'], coordinate['lng']], [table['latitude'][i], table['longitude'][i]])
            if d > radius * radius:
                pass
            else:
                temp = {'編號': i, '立案時間': '0', '派工項目': '0', '案件地址': '0', '經緯度': '0'}
                temp['立案時間'] = table['立案時間'][i]
                temp['派工項目'] = table['派工項目'][i]
                temp['案件地址'] = table['案件地址'][i]
                temp['經緯度'] = table['經緯度'][i]
                result.append(temp)
        return result

#output example:
#[{'編號': 146, '立案時間': '2016-03-02 17:23', '派工項目': '鄰里無主垃圾清運', '案件地址': '中山區錦州路', '經緯度': '(25.06039, 121.5337798)'},
# {'編號': 425, '立案時間': '2016-03-06 12:11', '派工項目': '鄰里無主垃圾清運', '案件地址': '中山區錦州街', '經緯度': '(25.06039, 121.5337798)'},
# {'編號': 667, '立案時間': '2016-03-09 08:49', '派工項目': '交通號誌異常', '案件地址': '中山區錦州街', '經緯度': '(25.06039, 121.5337798)'},
# {'編號': 707, '立案時間': '2016-03-09 16:15', '派工項目': '鄰里無主垃圾清運', '案件地址': '中山區錦州街', '經緯度': '(25.06039, 121.5337798)'},
# {'編號': 774, '立案時間': '2016-03-10 15:19', '派工項目': '道路油漬', '案件地址': '中山區長春路', '經緯度': '(25.0547633, 121.5362581)'}]

    def __calpoint(self, address, API_KEY):
        data = self.__search(address = address, API_KEY = API_KEY)
        result = {'衛生':0, '住宅安寧':0, '交通安全':0, '住宅安全': False}
        for i in data:
            try:
                if any(item in i["派工項目"] for item in ('垃圾', '散落')):
                    result['衛生'] += 1
                elif any(item in i["派工項目"] for item in ('坑洞', '結構', '樹')):
                    result['住宅安寧'] += 2   
                elif any(item in i["派工項目"] for item in ('道', '路燈', '蓋', '路面', '標誌')):
                    result["交通安全"] += 1
            except:
                pass
        result['住宅安全'] = self.__checkfixed(address)
        return result

    def exec(self, address, API_KEY):
        self.dataupdate()
        result = self.__calpoint(address = address, API_KEY = API_KEY)
        return result

#### 使用指南 : Initialize的時候 call check_database
# g = Backend()
# g.exec(address)
