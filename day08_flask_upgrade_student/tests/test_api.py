# tests/test_api.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import pytest
from app import app  # 导入你项目的Flask app实例

@pytest.fixture
def client():
    # 测试客户端
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

# 测试1：/health 返回200
def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200

# 测试2：未登录访问 /api/metrics 被拦截（302重定向登录页）
def test_metrics_no_login(client):
    resp = client.get("/api/metrics")
    # 未登录跳转 /login，状态码302
    assert resp.status_code == 302
    assert "/login" in resp.location

# 测试3：登录后访问 /api/metrics 正常返回ok、metrics字段
def test_metrics_logged(client):
    # 先登录，模拟登录接口提交账号密码
    login_resp = client.post("/login", data={"username": "student", "password": "day07"})
    print("登录状态码：", login_resp.status_code) 
    resp = client.get("/api/metrics")
    data = resp.get_json()
    assert resp.status_code == 200
    assert data["ok"] is True
    assert "metrics" in data

# 测试4：带参数Fashion筛选品类接口，返回筛选结果
def test_categories_filter_fashion(client):
    # 先登录
    login_resp = client.post("/login", data={"username": "student", "password": "day07"})
    print("登录状态码：", login_resp.status_code) 
    resp = client.get("/api/categories?category=Fashion")
    data = resp.get_json()
    print("完整返回数据：", data)
    assert resp.status_code == 200
    assert data["ok"] is True
    # 筛选后只有Fashion一条数据
    assert len(data["rows"]) == 1
    assert data["rows"][0]["偏好品类"] == "Fashion"