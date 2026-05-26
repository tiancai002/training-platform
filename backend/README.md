# 🎓 培训类平台 - Training Platform

> 综合性培训平台：课程管理 + 在线售卖 + 题库系统 + 社区互动

---

## 📋 项目概述

本平台同时涵盖 **课程售卖** 与 **课程管理** 两大业务板块，提供完整的在线培训解决方案。

### 核心功能

| 模块 | 功能描述 |
|------|----------|
| 📚 **题库系统** | 证书/等级筛选、错题本、收藏、刷题数据、每日一题、自主/随机组卷 |
| 🎬 **课程系统** | 直播课程、录播课程、证书关联筛选、课程预约 |
| 💰 **支付系统** | 课程/题库/一对一辅导在线购买 |
| 💬 **沟通系统** | 1 对 1 私聊、社区论坛 (类贴吧) |
| 👤 **个人中心** | 知识图谱 (学习进度)、数据统计、订单管理 |
| 📱 **多端同步** | PC 端 + 小程序端数据实时同步 |

---

## 🏗️ 技术架构

### 后端 (Backend)
- **框架**: Python FastAPI
- **数据库**: PostgreSQL + Redis
- **ORM**: SQLAlchemy
- **认证**: JWT
- **实时通信**: WebSocket (私聊/通知)

### 前端 (Frontend)
- **框架**: Vue 3 + Vite
- **UI 库**: Element Plus
- **状态管理**: Pinia
- **HTTP 客户端**: Axios

### 部署
- **容器化**: Docker + Docker Compose
- **反向代理**: Nginx
- **CI/CD**: GitHub Actions

---

## 📁 项目结构

```
training-platform/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── models/         # 数据模型
│   │   ├── services/       # 业务逻辑
│   │   └── utils/          # 工具函数
│   ├── config/             # 配置文件
│   └── migrations/         # 数据库迁移
│
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── components/     # 组件
│   │   ├── pages/          # 页面
│   │   ├── store/          # 状态管理
│   │   └── utils/          # 工具函数
│   └── public/             # 静态资源
│
├── docs/                   # 文档
├── scripts/                # 脚本
└── docker-compose.yml      # Docker 配置
```

---

## 🚀 快速开始

### 环境要求
- Python 3.9+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+

### 后端启动
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 前端启动
```bash
cd frontend
npm install
npm run dev
```

---

## 📅 开发计划

### 第一阶段：题库系统 (当前)
- [ ] 数据库设计
- [ ] 题库 API 开发
- [ ] 错题本功能
- [ ] 刷题统计
- [ ] 组卷功能

### 第二阶段：课程系统
- [ ] 课程管理
- [ ] 直播集成
- [ ] 录播播放
- [ ] 预约系统

### 第三阶段：支付与沟通
- [ ] 支付集成
- [ ] 私聊功能
- [ ] 社区论坛

### 第四阶段：小程序
- [ ] 小程序开发
- [ ] 数据同步

---

## 📄 许可证

MIT License
