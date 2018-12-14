import beautifulsoup
import requests
from . import webscraping

class Get_data(DatabaseManager):
  def __init__(self, address):
    self.address = address
    super().__init__()
    pass
  
  @staticmethod
  def log_changer(self):
    log = change(self.address)
    return log
  
  @staticmethod
  def update(self, url = '')
    database_check()
    database_update()
    pass
