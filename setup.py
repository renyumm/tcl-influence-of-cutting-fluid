'''
LastEditors: renyumm strrenyumm@gmail.com
Date: 2024-09-09 09:49:55
LastEditTime: 2024-09-12 09:00:43
FilePath: /tcl-influence-of-cutting-fluid/setup.py
'''
from src.api.app import app

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)