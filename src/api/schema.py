'''
LastEditors: renyumm strrenyumm@gmail.com
Date: 2024-09-10 11:37:50
LastEditTime: 2024-09-12 10:07:44
FilePath: /tcl-influence-of-cutting-fluid/src/api/schema.py
'''
from pydantic import BaseModel
from typing import Optional
import datetime

today = datetime.date.today()
todayd90 = today - datetime.timedelta(days=90)
today = today.strftime('%Y-%m-%d')
todayd90 = todayd90.strftime('%Y-%m-%d')

class plotItem(BaseModel):
    axis: Optional[list] = []
    sessionid: str
    

class formulaItem(BaseModel):
    anomalies: Optional[list] = []
    start_time: Optional[str] = todayd90
    end_time: Optional[str] = today
    sessionid: str
    axis: Optional[list] = []
    

class basicInfoItem(BaseModel):
    sessionid: str
    
