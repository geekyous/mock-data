# FastAPI 服务端项目

这是一个使用 Python FastAPI 框架快速搭建的服务端项目，包含了一个现代化的 Web 界面来访问和测试 API 接口。

## 功能特性

- 🚀 **FastAPI 后端**: 高性能的异步 Web 框架
- 🎨 **现代化 UI**: 使用 Bootstrap 5 和自定义 CSS 的美观界面
- 📊 **实时数据展示**: 用户列表、产品列表和统计信息
- 🔧 **API 测试**: 内置的 API 测试功能
- 📱 **响应式设计**: 支持移动端和桌面端
- 🔄 **实时更新**: 自动刷新数据和状态

## 项目结构

```
mock-data/
├── server/             # FastAPI 服务端项目目录
│   ├── main.py              # FastAPI 主应用文件
│   ├── start_server.py      # 服务启动脚本
│   ├── requirements.txt     # Python 依赖包
│   └── README.md           # 服务端项目文档
└── frontend/           # 前端项目目录
    ├── templates/          # HTML 模板目录
    │   └── index.html      # 主页面模板
    ├── static/             # 静态文件目录
    │   ├── css/
    │   │   └── style.css   # 自定义样式
    │   └── js/
    │       └── app.js      # 前端 JavaScript
    └── README.md           # 前端项目文档
```

## 安装和运行

### 1. 进入项目目录

```bash
cd server
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行服务

```bash
python start_server.py
```

或者直接运行主文件：

```bash
python main.py
```

或者使用 uvicorn 直接运行：

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. 访问应用

- **主页**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/api/health

## API 接口



### 系统信息

- `GET /api/health` - 健康检查

## 使用说明

### 1. 查看数据

打开浏览器访问 http://localhost:8000，页面会自动加载：


### 4. 查看 API 文档

访问 http://localhost:8000/docs 查看完整的 API 文档，可以：
- 查看所有可用的接口
- 在线测试 API
- 查看请求和响应格式

## 技术栈

### 后端
- **FastAPI**: 现代、快速的 Web 框架
- **Uvicorn**: ASGI 服务器
- **Jinja2**: 模板引擎

### 前端
- **Bootstrap 5**: CSS 框架
- **Font Awesome**: 图标库
- **原生 JavaScript**: 前端交互

### 开发工具
- **Python 3.7+**: 编程语言
- **pip**: 包管理器

## 自定义和扩展

### 添加新的 API 接口

在 `main.py` 中添加新的路由：

```python
@app.get("/api/new-endpoint")
async def new_endpoint():
    return {"message": "新接口"}
```

### 修改数据

编辑 `main.py` 中的 `mock_data` 字典来修改模拟数据。

### 自定义样式

修改 `static/css/style.css` 来自定义界面样式。

### 添加新功能

在 `static/js/app.js` 中添加新的 JavaScript 函数。

## 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 使用不同端口
   uvicorn main:app --port 8001
   ```

2. **依赖安装失败**
   ```bash
   # 升级 pip
   pip install --upgrade pip
   
   # 使用虚拟环境
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate     # Windows
   ```

3. **页面无法访问**
   - 检查服务是否正在运行
   - 确认端口号是否正确
   - 检查防火墙设置

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 许可证

MIT License
