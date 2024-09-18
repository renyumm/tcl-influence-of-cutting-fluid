'''
LastEditors: renyumm strrenyumm@gmail.com
Date: 2024-09-10 11:22:39
LastEditTime: 2024-09-18 10:55:09
FilePath: /tcl-influence-of-cutting-fluid/src/api/app.py
'''
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.api.schema import plotItem, formulaItem, basicInfoItem
from src.api.plot3d import plotdata
from src.api.formula import formula, fomula_default
from src.utils.minio_connector import copy_and_rename_folder
import yaml


# 1、创建一个 FastAPI 实例
app = FastAPI(docs_url=None)    #app对象
app.mount("/src/api/css", StaticFiles(directory="./src/api/css"), name="css")   #挂载目录

# 2、声明一个 源 列表；重点：要包含跨域的客户端 源
origins = ["*"]

# 3、配置 CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许访问的源
    allow_credentials=True,  # 支持 cookie
    allow_methods=["*"],  # 允许使用的请求方法
    allow_headers=["*"]  # 允许携带的 Headers
)
    
# 路由
@app.get("/", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/src/api/css/swagger-ui-bundle.js",
        swagger_css_url="/src/api/css/swagger-ui.css",
        )


@app.post("/ai/material/cutting-fluid/basic-info")
async def basic_info(item: basicInfoItem):
    '''
    基本信息
    '''
    item.sessionid = item.sessionid.replace(' ', '')
    print(item)
    copy_and_rename_folder('rym-best-fluid', 'rym-best-fluid', '/test/', f'/{item.sessionid}/') 
    
    with open('src/settings/data.yaml', 'r') as f:
        yml = yaml.safe_load(f)
        
    item.__dict__['axis'] = ['成品电导率', '成品浊度', '成品温度']
    
    plot3ddata = plotdata(item)
    plot3ddata = {
        "data": plot3ddata,
        "axis": item.axis+['异常率']
    }
    
    formuladata = fomula_default(item)
    
    bs = {
        "anomalies": yml['anomalies'],
        "axis": yml['qualities'],
        "formula": formuladata,
        "plot": plot3ddata,
    }
    
    return JSONResponse(content={"data": bs})


@app.post("/ai/material/cutting-fluid/3d-plot")
async def plot_data(item: plotItem):
    '''
    3D 图表数据
    '''
    item.sessionid = item.sessionid.replace(' ', '')
    print(item)
    if not item.axis:
        item.axis = ['成品电导率', '成品浊度', '成品温度']
    
    data = plotdata(item)
    data = {
        "data": data,
        "axis": item.axis+['异常率']
    }
    return JSONResponse(content={"data": data})


@app.post("/ai/material/cutting-fluid/formula")
async def formula_data(item: formulaItem):
    '''
    最佳配方数据
    '''
    item.sessionid = item.sessionid.replace(' ', '')
    print(item)
    if not item.axis:
        item.axis = ['成品电导率', '成品浊度', '成品温度']
        
    if not item.anomalies:
        item.anomalies = ['跳线', '断缝']

    formula_data = formula(item)
    plot_data = plotdata(item)
    
    
    data = {
        "formula": formula_data,
        "plot": {
            'data': plot_data, 
            'axis': item.axis+['异常率']
            }
    }
    return JSONResponse(content={"data": data})


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
