'''
LastEditors: renyumm strrenyumm@gmail.com
Date: 2024-09-11 14:02:57
LastEditTime: 2024-09-11 17:49:27
FilePath: /tcl-influence-of-cutting-fluid/src/api/plot3d.py
'''
from src.utils.minio_connector import client
from io import BytesIO
import pandas as pd


def plotdata(item):
    bucket_name = "rym-best-fluid"
    object_name = f"{item.sessionid}/modelmap.csv"
    response = client.get_object(bucket_name, object_name)
    csv_data = BytesIO(response.read())  # Read bytes from the response
    data = pd.read_csv(csv_data)
    data = data[item.axis+['异常率']].round(4).values.tolist()
    
    return data
    
    
    
    
    
    