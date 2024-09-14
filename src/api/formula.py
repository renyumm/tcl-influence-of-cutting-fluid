'''
LastEditors: renyumm strrenyumm@gmail.com
Date: 2024-09-10 17:36:01
LastEditTime: 2024-09-12 12:04:40
FilePath: /tcl-influence-of-cutting-fluid/src/api/formula.py
'''
import yaml
import copy
from src.utils.connector import Connector
from src.utils.minio_connector import client
from src.model import remark
import pandas as pd
import numpy as np
import dill
from io import BytesIO


def deal_df(df, tag):
    df['异常类型'] = df['异常类型'].apply(lambda x: 1 if x in tag else 0)
    df['柠檬酸'] = df['柠檬酸'].str.replace('转换阶段', '柠檬酸20g').str.replace('0', '柠檬酸0g')
    df['柠檬酸'] = df['柠檬酸'].str.replace('g', '').str.replace('柠檬酸', '')
    df.replace('#DIV/0!', np.nan, inplace=True)
    df['置换量'] = df['置换量'].str.rstrip('%').astype('float') / 100
    df['离子液添加量'] = df['离子液添加量'].str.rstrip('%').astype('float') /100
    df['成品浓度'] = df['成品浓度'].str.rstrip('%').astype('float') / 100
    df = df.apply(pd.to_numeric, errors='coerce')  # 转换成数字
    df.dropna(how='any', inplace=True)

    return df


def formula(item):
    '''
    :param item: formulaItem
    '''
    # 数据列
    with open('src/settings/data.yaml', 'r') as f:
        yml = yaml.safe_load(f)

    fields = yml['qualities'] + yml['formulation'] + [yml['tag']]
    fields = ','.join([f"`{x}`" for x in fields])

    # 异常类型
    itemcov = copy.deepcopy(item)
    itemcov.anomalies = ','.join([f"'{x}'" for x in item.anomalies])
    itemcov.__dict__['fields'] = fields

    # sql模板
    with open('src/sql/get_data.sql', 'r') as f:
        sql = f.read()

    sql = sql.format(**itemcov.__dict__)
    
    # 查询数据
    with open('src/settings/database.yaml', 'r') as f:
        config_yaml = yaml.safe_load(f)
        
    conn = Connector(config_yaml)
    data = conn.get_data(sql)
    data = deal_df(data, item.anomalies)
    conn.dispose()
        
    # 数据处理, 创建模型
    modelmap, best_best_formul = remark(data, yml['qualities'], yml['formulation'])
    
    # 检查 bucket 是否存在，不存在则创建
    if not client.bucket_exists(item.sessionid):
        client.make_bucket(item.sessionid)

    modelmap.to_csv(f'model/modelmap.csv', index=False)
    client.fput_object('rym-best-fluid', f'{item.sessionid}/modelmap.csv', 'model/modelmap.csv')
    
    with open('model/model.pkl', 'wb') as f:
        dill.dump(best_best_formul, f)
    client.fput_object('rym-best-fluid', f'{item.sessionid}/model.pkl', 'model/model.pkl')
        
    # 保存模型, 返回结果
    return best_best_formul


def fomula_default(item):
    bucket_name = "rym-best-fluid"
    object_name = f"{item.sessionid}/model.pkl"
    response = client.get_object(bucket_name, object_name)
    data = BytesIO(response.read())  # Read bytes from the response
    data = dill.load(data)
    
    return data


if __name__ == '__main__':
    class DictToClass:
        def __init__(self, data):
            """
            初始化类时，将字典中的键值对转化为类的属性
            """
            for key, value in data.items():
                setattr(self, key, value)  # 动态设置类属性
    item = {
        'sessionid': 'test',
        'anomalies': ['跳线', '断缝']
    }
    item = DictToClass(item)
    print(formula(item))