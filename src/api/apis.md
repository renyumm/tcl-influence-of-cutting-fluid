<!--
 * @LastEditors: renyumm strrenyumm@gmail.com
 * @Date: 2024-09-10 10:31:51
 * @LastEditTime: 2024-09-10 13:23:42
 * @FilePath: /tcl-influence-of-cutting-fluid/src/api/apis.md
-->
# 接口说明
Post /ai/material/cutting-fluid/formulation

body:
```json
{
    "anomalies": [],
    "start_time": "2024-09-10 10:31:51",
    "end_time": "2024-09-10 10:31:51",
}
```
response:
```json
{   
    "data": [
        {
            "性质": {"成品电导率": [1, 2], "成品PH值": [1, 2], "成品浓度": [1, 2]}, 
            "配方": {"柠檬酸": "80", "离子添加液比例": "20"}
        },
        {
            "性质": {"成品电导率": [1, 2], "成品PH值": [1, 2], "成品浓度": [1, 2]}, 
            "配方": {"柠檬酸": "80", "离子添加液比例": "20"}
        }
    ]
}
```

Post /ai/material/cutting-fluid/3d-plot
body:
```json
{
    "axis": "成品电导率-成品PH值-成品浓度", 
}
```

response:
```json
{
    "data": {
        "x": {"data": [], "name": "成品电导率"},
        "y": {"data": [], "name": "成品PH值"},
        "z": {"data": [], "name": "成品浓度"},
    },
    "title": "成品电导率-成品PH值-成品浓度交互作用图",
}
```

