import logger
from .backend import dataprocessor, webscraper
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import tkinter as tk
import argparse


logging.basicConfig(level=logging.DEBUG, format="[%(levelname)-0s] %(name)-0s >> %(message)-0s")
logger = logging.getLogger(__name__)

log_filename = datetime.datetime.now().strftime("log/tk%Y-%m-%d_%H_%M_%S.log")
console = logging.StreamHandler()
console.setLevel(logging.INFO)

formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def logger_config(debug, to_file=False):
    if debug:
        logging.config.dictConfig(dict_config)
        logging.info('Debug mode.')
    else:
        if to_file:
            dict_config['loggers']['mixer_music'] = ['player']
        else:
            dict_config['loggers']['mixer_music'] = ['music_mixer']

        logging.config.dictConfig(dict_config)
        logging.info('Release mode.')

# =============================
# Main Execution Here
# =============================

if __name__ = '__main__':
  # TK_GUI Creation
  while textbox :
    x = text # input from GUI
    log_ = webscraper.logchaging(x) # 經緯度
    
    data = webscraper.update()
    ### Adjust your function here ###
    params = {meters, exhitbit = 10 } #customize
    table = dataprocessor.exec(log_, data, params)
    
    Tk.show(table)
    while True:
      tk.mainloop()
     
