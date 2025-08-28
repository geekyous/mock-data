import mysql.connector
from pydantic import BaseModel


class DbInfo(BaseModel):
    host: str
    port: int
    user: str
    password: str
    database: str


class MockConnection:
    """模拟数据库连接类，用于测试环境"""

    def __init__(self):
        self.mock_data = {
            'single_project_code': ['PROJ001', 'PROJ002', 'PROJ003', 'PROJ004', 'PROJ005']
        }

    def cursor(self):
        return MockCursor(self.mock_data)

    def close(self):
        print("模拟连接已关闭")

    def commit(self):
        print("模拟提交事务")


class MockCursor:
    """模拟游标类"""

    def __init__(self, mock_data):
        self.mock_data = mock_data
        self.rowcount = 0

    def execute(self, query):
        print(f"模拟执行查询: {query}")
        if 'single_project_code' in query:
            self.rowcount = len(self.mock_data['single_project_code'])

    def executemany(self, query, data):
        print(f"模拟批量执行查询: {query}")
        if isinstance(data, (list, tuple)):
            self.rowcount = len(data)
        else:
            self.rowcount = 0

    def fetchall(self):
        result = [(code,) for code in self.mock_data['single_project_code']]
        print(f"模拟查询结果: {result}")
        return result

    def close(self):
        print("模拟游标已关闭")


def create_connection():
    """创建数据库连接"""
    try:
        conn = mysql.connector.connect(
            host=db.host,
            port=db.port,
            user=db.user,
            password=db.password,
            database=db.database,
            autocommit=True,  # 自动提交
            buffered=True,  # 使用缓冲游标
            connection_timeout=30  # 连接超时时间
        )
        return conn
    except mysql.connector.Error as err:
        print(f"数据库连接错误: {err}")
        raise err


def check_connection():
    """检查连接是否有效"""
    result = {}
    try:
        conn = create_connection()
        conn.ping(reconnect=True, attempts=3, delay=5)
        result['connected'] = True

    except mysql.connector.Error as err:
        print(f'创建数据库连接失败: {err}')
        result['connected'] = False
        result['err'] = str(err)
    return result


class DbInstance:
    """数据库实例信息"""

    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database


db = DbInstance('127.0.0.1', 3306, 'root', 'root', 'gwjjspaq')


def get_db_info():
    return db


def update_db_info(host, port, user, password, database):
    db.host = host
    db.port = port
    db.user = user
    db.password = password
    db.database = database
