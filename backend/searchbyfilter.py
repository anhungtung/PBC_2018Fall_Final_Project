import logger
from database import Get_data
import math


#'user' and 'target' must be a list that have two items which is "longtitude" and "latitude"
def calculate_distance(user, target):
    #R -> radius of earth
    #need Absolute
    R = 6371000
    d = R * math.acos(math.sin(user[0])*math.sin(target[0]) + math.cos(user[0])*math.cos(target[0])*math.cos(target[1]-user[1]))
    return d

def search(address, radius=500):
    table = pd.read_csv('total_database.csv')
    
    #address -> coordinate
    coordinate = Get_data.log_changer(address)

    #calaculate the address 500m edge
    distance = radius*9/1000000
    top = coordinate[0] + distance
    bot = coordinate[0] - distance
    east = coordinate[1] + distance
    west = coordinate[1] - distance

    #filter the database
    table = table[(table["longtitude"].between(bot, top)) & (table["latitude"].between(west, east))]

    #calculate the distance and delete the coordinate that distance is larger than 'radius' and format to dictionary
    drop_list = []
    for i in range(table.count()):
        target = [table['longtitude'][i], table['latitude'][i]]
        if calculate_distance(coordinate, target) < radius:
            drop_list.append(i)
        else:
            pass
    table = list(table.drop(drop_list).values())

    return table
            
