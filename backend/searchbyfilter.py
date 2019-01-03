import logger
from database import Get_data
import math
import pandas

#'user' and 'target' must be a list that have two items which is "longtitude" and "latitude"
def calculate_distance(user, target):
    #R -> radius of earth
    la1, long1 = [math.pi/180*x for x in user]
    la2, long2 = [math.pi/180*x for x in target]
    R = 6371000
    d = R * math.acos(math.sin(la1)*math.sin(la2) + math.cos(la1)*math.cos(la2)*math.cos(long2-long1))
    return d

def search(address, radius=500):
    table = pd.read_csv('total_database.csv')
    
    #address -> coordinate
    coordinate = Get_data.log_changer(address)

    #calculate the distance and delete the coordinate that distance is larger than 'radius' and format to dictionary
    result = []
    for i in list(table.index):
        d = calculate_distance(coordinate, [table['latitude'][i], table['longitude'][i]])
        if d > radius:
            pass
        else:
            temp = {}
            #temp = {'編號': i, '立案時間': table['立案時間'][i], '派工項目': table['派工項目'][i], '案件地址': table['案件地址'], '經緯度': table['經緯']}
            temp['編號'] = i
            temp['立案時間'] = table['立案時間'][i]
            temp['派工項目'] = table['派工項目'][i]
            temp['案件地址'] = table['案件地址'][i]
            temp['經緯度'] = table['經緯'][i]
            result.append(temp)

    return result
