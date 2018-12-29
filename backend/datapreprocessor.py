import logger
from database import Get_Data

logging.basicConfig(level=logging.DEBUG, format="[%(levelname)-0s] %(name)-0s >> %(message)-0s")
logger = logging.getLogger(__name__)

class Exec:
    def __init__(self):
    pass
    
    def exec():
        table = pd.read_csv('total_database.csv',encoding="big5")
        table.columns=["number",'Reason','address','time']

        table["type"] = np.nan 
        table["point"] = np.nan
    def cal_type(row):
        if "清" in row["Reason"]:
            row['type'] = "衛生"
            row['point'] = 1

        elif "噪音"in  row["Reason"]:
            row['type'] = "住宅安寧"  
            row['point'] = 2     
        elif "海砂屋"in row["Reason"]:
            row['type'] = "住宅安全"    
            row['point'] = True 
        else:
            row['type'] = "交通安全"  
            row['point'] = 1

        return row
    table = table.apply(cal_type, axis=1)
   
    table['log'] = Get_Data.log_changer(table['address'])
    #coding_here
