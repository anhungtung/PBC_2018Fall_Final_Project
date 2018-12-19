import logger
from database import Get_Data

logging.basicConfig(level=logging.DEBUG, format="[%(levelname)-0s] %(name)-0s >> %(message)-0s")
logger = logging.getLogger(__name__)

class Exec:
  def __init__(self):
    pass
    
  def exec():
    table = pd.read_csv('......')
   
    table['log'] = Get_Data.log_changer(table['address'])
    #coding_here
