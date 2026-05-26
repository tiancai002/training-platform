#!/usr/bin/env python3
"""
培训平台 - 自动测试与迭代脚本
每 10 分钟运行一轮测试，自动发现问题并优化
"""
import sys
import os
import json
import time
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# 配置
BASE_URL = "http://localhost:8000"
TEST_USER = "demo"
TEST_PASS = "demo123456"
LOG_FILE = "/var/www/training-platform/logs/auto_test.log"

def log(message):
    """写入日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] {message}\n"
    print(log_msg.strip())
    with open(LOG_FILE, 'a') as f:
        f.write(log_msg)

def api_request(endpoint, method='GET', data=None, headers=None):
    """发送 API 请求"""
    url = f"{BASE_URL}{endpoint}"
    if headers is None:
        headers = {}
    
    if data and method == 'POST':
        data = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    
    req = Request(url, data=data, headers=headers, method=method)
    
    try:
        with urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode('utf-8'))
    except HTTPError as e:
        return {"error": e.code, "message": e.reason}
    except URLError as e:
        return {"error": "connection", "message": str(e)}

def get_token():
    """获取测试 Token"""
    # 使用表单格式登录
    import urllib.request
    import urllib.parse
    
    url = f"{BASE_URL}/api/auth/login"
    data = urllib.parse.urlencode({'username': TEST_USER, 'password': TEST_PASS}).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            if 'access_token' in result:
                return result['access_token']
    except Exception as e:
        log(f"  登录异常：{e}")
    return None

def test_auth():
    """测试认证模块"""
    log("【测试】认证模块")
    
    # 登录测试
    token = get_token()
    if token:
        log("  ✓ 登录成功")
        
        # 获取用户信息
        result = api_request('/api/auth/me', headers={'Authorization': f'Bearer {token}'})
        if 'username' in result:
            log("  ✓ 获取用户信息成功")
            return True, token
        else:
            log(f"  ✗ 获取用户信息失败：{result}")
            return False, token
    else:
        log("  ✗ 登录失败")
        return False, None

def test_question_bank(token):
    """测试题库模块"""
    log("【测试】题库模块")
    
    # 题库列表
    result = api_request('/api/question/banks')
    if isinstance(result, list) and len(result) > 0:
        log(f"  ✓ 题库列表：{len(result)} 个")
    else:
        log(f"  ✗ 题库列表失败：{result}")
        return False
    
    # 题目列表
    result = api_request('/api/question/questions?bank_id=1&page=1')
    if 'items' in result:
        log(f"  ✓ 题目列表：{result.get('total', 0)} 道")
    else:
        log(f"  ✗ 题目列表失败：{result}")
        return False
    
    # 每日一题
    result = api_request('/api/question/daily', headers={'Authorization': f'Bearer {token}'})
    if 'question' in result or 'detail' not in result:
        log("  ✓ 每日一题正常")
    else:
        log(f"  ⚠ 每日一题异常：{result}")
    
    # 刷题统计
    result = api_request('/api/question/stats', headers={'Authorization': f'Bearer {token}'})
    if 'total_questions' in result:
        log(f"  ✓ 刷题统计：{result['total_questions']} 道")
    else:
        log(f"  ⚠ 刷题统计异常：{result}")
    
    return True

def test_courses():
    """测试课程模块"""
    log("【测试】课程模块")
    
    result = api_request('/api/course/list')
    if 'items' in result:
        log(f"  ✓ 课程列表：{result.get('total', 0)} 个")
        return True
    else:
        log(f"  ✗ 课程列表失败：{result}")
        return False

def test_community(token):
    """测试社区模块"""
    log("【测试】社区模块")
    
    # 帖子列表
    result = api_request('/api/community/posts')
    if 'items' in result:
        log(f"  ✓ 帖子列表：{result.get('total', 0)} 个")
    else:
        log(f"  ✗ 帖子列表失败：{result}")
        return False
    
    # 分类列表
    result = api_request('/api/community/categories')
    if isinstance(result, list):
        log(f"  ✓ 分类列表：{len(result)} 个")
    else:
        log(f"  ⚠ 分类列表异常：{result}")
    
    return True

def generate_report(test_results):
    """生成测试报告"""
    log("\n" + "="*50)
    log("【测试报告】")
    log("="*50)
    
    total = len(test_results)
    passed = sum(1 for r in test_results if r[1])
    
    for name, passed, details in test_results:
        status = "✓" if passed else "✗"
        log(f"{status} {name}")
    
    log("="*50)
    log(f"总计：{passed}/{total} 通过")
    log("="*50)
    
    return passed == total

def auto_optimize():
    """自动优化建议"""
    log("\n【优化建议】")
    
    # 检查题目数量
    result = api_request('/api/question/banks')
    if isinstance(result, list):
        total_questions = sum(b.get('total_questions', 0) for b in result)
        if total_questions < 200:
            log("  ⚠ 题目数量较少，建议增加")
        else:
            log(f"  ✓ 题目数量充足：{total_questions} 道")
    
    # 检查课程数量
    result = api_request('/api/course/list')
    if 'total' in result:
        if result['total'] < 10:
            log("  ⚠ 课程数量较少，建议增加")
        else:
            log(f"  ✓ 课程数量充足：{result['total']} 个")
    
    # 检查社区活跃度
    result = api_request('/api/community/posts')
    if 'total' in result:
        if result['total'] < 20:
            log("  ⚠ 社区帖子较少，建议增加")
        else:
            log(f"  ✓ 社区帖子充足：{result['total']} 个")

def main():
    """主函数"""
    log("\n" + "="*50)
    log("培训平台 - 自动测试开始")
    log("="*50)
    
    test_results = []
    
    # 1. 测试认证
    auth_ok, token = test_auth()
    test_results.append(("认证模块", auth_ok, ""))
    
    if token:
        # 2. 测试题库
        qb_ok = test_question_bank(token)
        test_results.append(("题库模块", qb_ok, ""))
        
        # 3. 测试课程
        course_ok = test_courses()
        test_results.append(("课程模块", course_ok, ""))
        
        # 4. 测试社区
        comm_ok = test_community(token)
        test_results.append(("社区模块", comm_ok, ""))
    else:
        test_results.append(("题库模块", False, "认证失败"))
        test_results.append(("课程模块", False, "认证失败"))
        test_results.append(("社区模块", False, "认证失败"))
    
    # 生成报告
    all_passed = generate_report(test_results)
    
    # 优化建议
    auto_optimize()
    
    log("\n下一轮测试将在 10 分钟后...")
    
    return all_passed

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"【错误】{str(e)}")
        import traceback
        log(traceback.format_exc())
