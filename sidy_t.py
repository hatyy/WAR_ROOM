# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 12:04:34 2020

@author: sidyndiaye
"""





import pyodbc
import numpy as np
import pandas as pd
import datetime as dt
from datetime import date

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=BOC-DB;'
                      'Database=BD_THIERNO_SIDY_ST201908_WARR_ROOM;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
req=cursor.execute('SELECT * FROM ALL_GROSS')

columns = cursor.description 
result = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
df= pd.DataFrame(result)



df['Territory'] = np.where((df.Territory == 'Dakar ville'),'DAKAR VILLE',df.Territory)
df['Territory'] = np.where((df.Territory == 'Free Dakar Ville'),'DAKAR VILLE',df.Territory)
df['Territory'] = np.where((df.Territory == 'Tigo Dakar Ville'),'DAKAR VILLE',df.Territory)
df['Territory'] = np.where((df.Territory == 'Free Banlieue'),'DAKAR BANLIEUE',df.Territory)
df['Territory'] = np.where((df.Territory == 'Tigo Banlieue'),'DAKAR BANLIEUE',df.Territory)
df['Territory'] = np.where((df.Territory == 'Tigo CENTRE'),' CENTRE',df.Territory)
df['Territory'] = np.where((df.Territory == 'Free CENTRE'),' CENTRE',df.Territory)
df['Territory'] = np.where((df.Territory == 'Free CENTRE-OUEST'),' CENTRE-OUEST',df.Territory)
df['Territory'] = np.where((df.Territory == 'Tigo CENTRE-OUEST'),' CENTRE-OUEST',df.Territory)
df['Territory'] = np.where((df.Territory == 'Free NORD'),' NORD',df.Territory)
df['Territory'] = np.where((df.Territory == 'Free NORD'),' NORD',df.Territory)
df['Territory'] = np.where((df.Territory == 'Free NORD-EST'),' NORD-EST',df.Territory)
df['Territory'] = np.where((df.Territory == 'Tigo NORD-EST'),' NORD-EST',df.Territory)
df['Territory'] = np.where((df.Territory == 'Tigo SUD'),' SUD',df.Territory)
df['Territory'] = np.where((df.Territory == 'Free SUD'),' SUD',df.Territory)
df['Territory'] = np.where((df.Territory == 'Free EST'),' EST',df.Territory)



df_obj =pd.read_csv('C:\\Users\\sidyndiaye\\Desktop\\dash_h\\objectifs_gross.csv',sep=';')

df['Territory'] = df['Territory'].str.lstrip()
df['Territory'] = df['Territory'].str.rstrip()




del df['FullName'],df['PhoneNumber'],df['type'],df['ROLE'],df['TigoCode'],df['ZONE_COM'],df['TeamLeader'],df['SalesCoordinator']





df.sale_date=pd.to_datetime(df.sale_date,format='%Y-%m-%d')

t=dt.datetime.today().strftime("%Y")

##Period_2020

maxs = max(df.sale_date)
mins = '2020-01-01 00:00:00'
minss= pd.to_datetime(mins,format='%Y-%m-%d')
periode = pd.period_range(start=minss, end=maxs, freq='D')
period_2020 = (df['sale_date']>= minss) & (df['sale_date']<= maxs)
df_2020=df[period_2020]

df_2020['Year'] = pd.DatetimeIndex(df_2020['sale_date']).year
df_2020['MonthNum']=df_2020['sale_date'].dt.month
del df_2020['sale_date']
df_2020 = df_2020.groupby(['Year','MonthNum','Territory']).sum()#.reset_index()
df_2020_year = df_2020.groupby(['Year','MonthNum','Territory']).sum()
df_2020['PREV%'] = df_2020.pct_change(10)
df_2020=df_2020.reset_index()




    
max_=date(maxs.year - 1, maxs.month, maxs.day).strftime('%Y-%m-%d')
max_2019=minss= pd.to_datetime(max_,format='%Y-%m-%d')
min_='2019-01-01 00:00:00'
min_2019= pd.to_datetime(min_,format='%Y-%m-%d')
period_2019 = (df['sale_date']>= min_2019) & (df['sale_date']<= max_2019)
df_2019=df[period_2019]
df_2019['Year'] = pd.DatetimeIndex(df_2019['sale_date']).year
df_2019['MonthNum']=df_2019['sale_date'].dt.month
del df_2019['sale_date']
df_2019 = df_2019.groupby(['Year','MonthNum','Territory']).sum()#.reset_index()
df_2019_year = df_2019.groupby(['Year','MonthNum','Territory']).sum()
df_2019['PREV%'] = df_2019.pct_change(10)
df_2019=df_2019.reset_index()
##Period 2018
max_1=date(max_2019.year - 1, max_2019.month, max_2019.day).strftime('%Y-%m-%d')
max_2018=minss= pd.to_datetime(max_1,format='%Y-%m-%d')
min_s='2018-01-01 00:00:00'
min_2018= pd.to_datetime(min_s,format='%Y-%m-%d')
period_2018 = (df['sale_date']>= min_2018) & (df['sale_date']<= max_2018)
df_2018=df[period_2018]

df_2018['Year'] = pd.DatetimeIndex(df_2018['sale_date']).year
df_2018['MonthNum']=df_2018['sale_date'].dt.month
del df_2018['sale_date']
df_2018 = df_2018.groupby(['Year','MonthNum','Territory']).sum()#.reset_index()
df_2018_year = df_2018.groupby(['Year','MonthNum','Territory']).sum()
df_2018['PREV%'] = df_2018.pct_change(5)
df_2018=df_2018.reset_index()

### df totale
dft =(df_2019.append(df_2020))#.append(df_2018)
##final df
df=dft
df=df.fillna(0)
df['MOM%'] = ((df['PREV%'])*100).round(decimals=2)
del df['PREV%']
#df = df.groupby([df['sale_date'],df['Territory']],as_index=False).sum()
df_yearr=dft =(df_2019_year.append(df_2020_year))
df_yearr['PREV%'] = df_yearr.pct_change(30)
df_yearr=df_yearr.fillna(0)
df_yearr=df_yearr.reset_index()
df_yearr['YOY%'] = ((df_yearr['PREV%'])*100).round(decimals=2)
del df_yearr['PREV%']

df = pd.merge(df,df_yearr, on =['Territory','MonthNum','Year','GROSS'])

df['MonthNum']=df['MonthNum'].map({1:'Janvier',2:'Fevrier',3:'Mars',4:'Avril',
  5:'Mai',6:'Juin',7:'Juillet',8:'Aout',9:'Septembre',10:'Octobre',11:'Novembre',12:'Decembre'})

#rename Monthname
df.columns = df.columns.str.replace('MonthNum', 'Month')
df_obj =pd.read_csv('C:\\Users\\sidyndiaye\\Desktop\\dash_h\\objectifs_gross.csv',sep=';', encoding = "ISO-8859-1", engine='python')
all_m = pd.merge(df,df_obj,on=['Year','Territory','Month'])
all_m['R/O'] = ((all_m['GROSS']) / (all_m['objectifs'].astype(int))).round(decimals=2)












