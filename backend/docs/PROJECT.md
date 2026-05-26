# 培训平台项目文档

## 📋 项目概述

### 项目定位
综合性培训平台，同时涵盖 **课程售卖** 与 **课程管理** 两大业务板块。

### 目标用户
- 学员：在线学习、刷题、获取证书
- 讲师：课程发布、直播授课、一对一辅导
- 管理员：平台运营、内容管理

---

## 🏗️ 系统架构

### 技术栈

#### 后端
| 组件 | 技术 | 说明 |
|------|------|------|
| 框架 | FastAPI | 高性能 Python Web 框架 |
| 数据库 | PostgreSQL | 主数据库 |
| 缓存 | Redis | 会话缓存、实时数据 |
| ORM | SQLAlchemy | 数据库操作 |
| 认证 | JWT | Token 认证 |
| 实时通信 | WebSocket | 私聊、通知 |

#### 前端
| 组件 | 技术 | 说明 |
|------|------|------|
| 框架 | Vue 3 | 组合式 API |
| 构建工具 | Vite | 快速开发构建 |
| UI 库 | Element Plus | 组件库 |
| 状态管理 | Pinia | 轻量级状态管理 |
| 路由 | Vue Router | 前端路由 |
| HTTP | Axios | API 请求 |

---

## 📁 目录结构

```
training-platform/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── api/               # API 路由
│   │   │   ├── auth.py        # 认证 API
│   │   │   ├── user.py        # 用户 API
│   │   │   ├── question.py    # 题库 API
│   │   │   ├── course.py      # 课程 API
│   │   │   ├── order.py       # 订单 API
│   │   │   ├── chat.py        # 聊天 API
│   │   │   └── community.py   # 社区 API
│   │   ├── models/            # 数据模型
│   │   │   ├── user.py        # 用户模型
│   │   │   ├── certificate.py # 证书模型
│   │   │   ├── question.py    # 题目模型
│   │   │   ├── course.py      # 课程模型
│   │   │   ├── order.py       # 订单模型
│   │   │   ├── chat.py        # 聊天模型
│   │   │   └── community.py   # 社区模型
│   │   ├── services/          # 业务逻辑
│   │   └── utils/             # 工具函数
│   ├── config/
│   │   ├── settings.py        # 配置管理
│   │   └── database.py        # 数据库配置
│   ├── schemas/               # Pydantic 模式
│   └── requirements.txt       # Python 依赖
│
├── frontend/                   # 前端应用
│   ├── src/
│   │   ├── api/               # API 客户端
│   │   ├── components/        # 公共组件
│   │   ├── pages/             # 页面组件
│   │   │   ├── Home.vue       # 首页
│   │   │   ├── Login.vue      # 登录
│   │   │   ├── Register.vue   # 注册
│   │   │   ├── QuestionBank.vue # 题库
│   │   │   ├── Practice.vue   # 练习
│   │   │   ├── WrongBook.vue  # 错题本
│   │   │   ├── Courses.vue    # 课程
│   │   │   ├── Community.vue  # 社区
│   │   │   └── Profile.vue    # 个人中心
│   │   ├── router/            # 路由配置
│   │   ├── store/             # 状态管理
│   │   └── utils/             # 工具函数
│   └── package.json
│
└── docs/                       # 文档
```

---

## 🗄️ 数据库设计

### 核心表

#### 用户表 (users)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| username | String | 用户名 |
| email | String | 邮箱 |
| password_hash | String | 密码哈希 |
| role | Enum | 角色 (admin/instructor/student) |
| learning_stats | JSON | 学习统计缓存 |

#### 证书表 (certificates)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| name | String | 证书名称 |
| level | Enum | 等级 (basic/intermediate/advanced/expert) |
| type | Enum | 类型 (professional/skill/training) |

#### 题库表 (question_banks)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| name | String | 题库名称 |
| certificate_id | Integer | 关联证书 |
| total_questions | Integer | 题目总数 |

#### 题目表 (questions)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| content | Text | 题目内容 |
| options | JSON | 选项 |
| answer | String | 答案 |
| difficulty | String | 难度 |
| tags | JSON | 标签 |

#### 错题表 (wrong_questions)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| user_id | Integer | 用户 ID |
| question_id | Integer | 题目 ID |
| wrong_count | Integer | 答错次数 |
| correct_count | Integer | 答对次数 |
| remove_threshold | Integer | 移除阈值 |

---

## 🔌 API 接口

### 认证模块
```
POST   /api/auth/register    # 用户注册
POST   /api/auth/login       # 用户登录
GET    /api/auth/me          # 获取当前用户
```

### 题库模块
```
GET    /api/question/banks           # 获取题库列表
GET    /api/question/banks/{id}      # 获取题库详情
GET    /api/question/questions       # 获取题目列表
POST   /api/question/practice        # 开始练习
POST   /api/question/practice/submit # 提交答案
GET    /api/question/wrong-book      # 获取错题本
GET    /api/question/daily           # 每日一题
GET    /api/question/stats           # 练习统计
```

### 课程模块
```
GET    /api/course/list        # 课程列表
GET    /api/course/{id}        # 课程详情
POST   /api/course/enroll      # 报名课程
```

### 订单模块
```
POST   /api/order/create       # 创建订单
GET    /api/order/list         # 订单列表
GET    /api/order/{id}         # 订单详情
```

### 社区模块
```
GET    /api/community/posts          # 帖子列表
POST   /api/community/posts/create   # 创建帖子
GET    /api/community/posts/{id}     # 帖子详情
POST   /api/community/posts/{id}/like # 点赞
POST   /api/community/posts/{id}/comment # 评论
```

---

## 🚀 开发计划

### 第一阶段：题库系统 (当前优先级)
- [x] 数据库模型设计
- [x] 题库 API 开发
- [x] 前端页面框架
- [ ] 错题本完整功能
- [ ] 练习模式实现
- [ ] 刷题统计图表
- [ ] 组卷功能

### 第二阶段：课程系统
- [ ] 课程管理 CRUD
- [ ] 直播集成 (第三方/自建)
- [ ] 录播视频播放
- [ ] 课程预约系统
- [ ] 学习进度跟踪

### 第三阶段：支付与沟通
- [ ] 支付接口集成 (微信/支付宝)
- [ ] 1 对 1 私聊 (WebSocket)
- [ ] 社区论坛完整功能
- [ ] 通知系统

### 第四阶段：小程序
- [ ] 小程序开发
- [ ] 数据同步机制
- [ ] 移动端优化

---

## 📦 部署

### Docker 部署
```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 环境变量
```bash
# .env
DATABASE_URL=postgresql://user:pass@localhost:5432/training_platform
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
```

---

## 📝 开发规范

### 代码规范
- Python: PEP 8
- JavaScript: ESLint + Airbnb
- Vue: Vue Style Guide

### Git 规范
```
feat: 新功能
fix: 修复 bug
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试
chore: 构建/工具
```

---

## 🔐 安全考虑

- JWT Token 认证
- 密码 bcrypt 加密
- CORS 配置
- SQL 注入防护 (ORM)
- XSS 防护
- 请求频率限制

---

## 📞 联系方式

项目开发团队
