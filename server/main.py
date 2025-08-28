import json
from datetime import datetime
from http.client import HTTPException
from typing import List

import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import sql
from mock import Mock, ThreeKind

# 创建FastAPI应用实例
app = FastAPI(
    title="仿真数据 服务端",
    description="一个简单的FastAPI服务端示例",
    version="1.0.0"
)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# 设置模板目录
templates = Jinja2Templates(directory="frontend/templates")


# 请求模型
class GenerateDataRequest(BaseModel):
    plan_start_time: str
    plan_end_time: str


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """主页"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "message": "服务运行正常"
    }


@app.get("/api/db/config")
async def get_db_config():
    """获取数据库配置接口"""
    return {
        "success": True,
        "message": "所有仿真数据生成成功",
        "data": sql.db
    }


@app.post("/api/db/config")
async def save_db_config(db_info: sql.DbInfo):
    """获取数据库配置接口"""
    sql.update_db_info(db_info.host, db_info.port, db_info.user, db_info.password, db_info.database)
    return {
        "success": True,
        "message": "数据库信息保存成功",
        "data": sql.db
    }


@app.get("/api/db/connect/test")
async def test_db_connect():
    """获取数据库配置接口"""
    test_result = sql.check_connection()
    return {
        "success": True,
        "message": "",
        "data": test_result
    }


@app.post("/api/generate/all-data")
async def generate_all_data(request: GenerateDataRequest):
    if request.plan_start_time is None or request.plan_end_time is None:
        raise HTTPException(status_code=400, detail="开始时间和结束时间不能为空")
    if request.plan_start_time >= request.plan_end_time:
        raise HTTPException(status_code=400, detail="开始时间必须小于结束时间")

    """批量生成所有仿真数据"""
    try:
        mock = Mock()
        result = mock.generate_data(request.plan_start_time, request.plan_end_time)
        return {
            "success": True,
            "message": "所有仿真数据生成成功",
            "data": result
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"批量生成失败: {str(e)}",
            "data": None
        }


@app.post("/supervision/team/member/downloadSgryData")
async def team_member(param: ThreeKind):
    """三种人评分"""
    mock = Mock()
    data = mock.three_kind(param)
    return {
        "data": data,
        "code": 0,
        "msg": "服务运行正常"
    }


@app.post("/raw-json")
async def receive_raw_json(request: Request):
    # 获取原始请求体
    body = await request.body()
    body_str = body.decode('utf-8')
    data = json.loads(body_str)

    print(f"原始请求体: {data}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
