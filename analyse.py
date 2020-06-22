# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 08:17:17 2020

@author: sidyndiaye
"""


#from datetime import date


import pyodbc

import pandas as pd





conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=BOC-DB;'
                      'Database=BD_THIERNO_SIDY_ST201908_WARR_ROOM;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
req=cursor.execute('SELECT top 1000 * from [BALANCE_DEARLER]')

columns = cursor.description 
result = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
df= pd.DataFrame(result)
