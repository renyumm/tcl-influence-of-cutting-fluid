'''
LastEditors: renyumm strrenyumm@gmail.com
Date: 2024-09-10 11:37:50
LastEditTime: 2024-09-11 18:00:47
FilePath: /tcl-influence-of-cutting-fluid/src/api/schema.py
'''
from pydantic import BaseModel


class plotItem(BaseModel):
    axis: list
    sessionid: str
    

class formulaItem(BaseModel):
    anomalies: list
    start_time: str
    end_time: str
    sessionid: str
    axis: list
    
    class Config:
        extra = "allow"  # 允许动态添加额外字段
    

class basicInfoItem(BaseModel):
    sessionid: str
    
