import logger
from database import Get_Data

logging.basicConfig(level=logging.DEBUG, format="[%(levelname)-0s] %(name)-0s >> %(message)-0s")
logger = logging.getLogger(__name__)
import pandas as pd
import numpy as np
class Exec:
    def __init__(self):
    pass
    
    def exec():
        table = pd.read_csv("1999_data.csv")#先指定第一行為indexcolumn

        table = table.rename(columns={'0':'經緯'})
        table["longitude"] =np.nan
        table["laitude"] = np.nan
        table["longitude"] = table['經緯'].str.split(",").str.get(0).str.lstrip( "(" )
        table["laitude"] = table['經緯'].str.split(",").str.get(1).str.rstrip( ")" )
        #把經緯度分開欄位
        table = table.to_csv("1999_data.csv")#儲存檔案
        return table
   
  
