#!/usr/bin/env python3
"""
FastAPI 服务启动脚本
"""

import uvicorn
import sys
import os
from sql import DbInfo


def main():
    """启动 FastAPI 服务"""
    print("🚀 启动 FastAPI 服务端...")
    print("📁 项目目录:", os.getcwd())
    print("🌐 服务地址: http://localhost:8000")
    print("📚 API文档: http://localhost:8000/docs")
    print("💚 健康检查: http://localhost:8000/api/health")
    print("=" * 50)


    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
