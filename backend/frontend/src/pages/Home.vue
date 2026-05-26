<template>
  <div class="home">
    <!-- Top Navigation -->
    <header class="header">
      <div class="header-content">
        <div class="logo">
          <span class="logo-icon">🎓</span>
          <span class="logo-text">培训平台</span>
        </div>
        <nav class="nav">
          <router-link to="/question-bank" class="nav-item">
            <el-icon><Document /></el-icon>
            <span>题库</span>
          </router-link>
          <router-link to="/courses" class="nav-item">
            <el-icon><VideoCamera /></el-icon>
            <span>课程</span>
          </router-link>
          <router-link to="/community" class="nav-item">
            <el-icon><ChatDotRound /></el-icon>
            <span>社区</span>
          </router-link>
        </nav>
        <div class="auth">
          <template v-if="userStore.isLoggedIn">
            <router-link to="/profile" class="user-link">
              <el-avatar :size="32" :src="userStore.user?.avatar_url" icon="User" />
              <span>{{ userStore.user?.nickname || userStore.user?.username }}</span>
            </router-link>
            <el-button @click="userStore.logout" size="small" circle>
              <el-icon><SwitchButton /></el-icon>
            </el-button>
          </template>
          <template v-else>
            <router-link to="/login">
              <el-button size="small">登录</el-button>
            </router-link>
            <router-link to="/register">
              <el-button type="primary" size="small">注册</el-button>
            </router-link>
          </template>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main">
      <!-- Hero Section -->
      <section class="hero">
        <div class="hero-content">
          <h1 class="hero-title">
            <span class="gradient-text">提升技能 · 成就未来</span>
          </h1>
          <p class="hero-subtitle">专业证书培训 · 智能题库 · 精品课程 · 学习社区</p>
          <div class="cta">
            <router-link to="/question-bank">
              <el-button type="primary" size="large" round>
                <el-icon><Document /></el-icon>
                开始刷题
              </el-button>
            </router-link>
            <router-link to="/courses">
              <el-button size="large" round>
                <el-icon><VideoCamera /></el-icon>
                浏览课程
              </el-button>
            </router-link>
          </div>
        </div>
        <div class="hero-decoration">
          <div class="floating-card c1">📚</div>
          <div class="floating-card c2">💡</div>
          <div class="floating-card c3">🎯</div>
          <div class="floating-card c4">⭐</div>
        </div>
      </section>

      <!-- Feature Cards (Clickable) -->
      <section class="features">
        <div class="section-title">
          <h2>核心功能</h2>
          <p>一站式学习平台，助你快速成长</p>
        </div>
        <el-row :gutter="24">
          <el-col :span="8">
            <router-link to="/question-bank" class="feature-link">
              <el-card class="feature-card feature-question" shadow="hover">
                <div class="feature-icon">📝</div>
                <h3>智能题库</h3>
                <p class="feature-desc">9 个题库 · 258 道精选题目</p>
                <p class="feature-detail">按证书等级筛选，智能错题本，高效刷题</p>
                <div class="feature-stats">
                  <div class="stat">
                    <span class="stat-value">9</span>
                    <span class="stat-label">题库</span>
                  </div>
                  <div class="stat">
                    <span class="stat-value">258</span>
                    <span class="stat-label">题目</span>
                  </div>
                  <div class="stat">
                    <span class="stat-value">89%</span>
                    <span class="stat-label">通过率</span>
                  </div>
                </div>
                <div class="feature-action">
                  <el-button type="primary" round size="small">
                    进入题库 <el-icon><ArrowRight /></el-icon>
                  </el-button>
                </div>
              </el-card>
            </router-link>
          </el-col>
          <el-col :span="8">
            <router-link to="/courses" class="feature-link">
              <el-card class="feature-card feature-course" shadow="hover">
                <div class="feature-icon">🎬</div>
                <h3>精品课程</h3>
                <p class="feature-desc">18 门精选优质课程</p>
                <p class="feature-detail">直播录播结合，专业讲师授课</p>
                <div class="feature-stats">
                  <div class="stat">
                    <span class="stat-value">18</span>
                    <span class="stat-label">课程</span>
                  </div>
                  <div class="stat">
                    <span class="stat-value">3000+</span>
                    <span class="stat-label">学员</span>
                  </div>
                  <div class="stat">
                    <span class="stat-value">4.9</span>
                    <span class="stat-label">评分</span>
                  </div>
                </div>
                <div class="feature-action">
                  <el-button type="primary" round size="small">
                    浏览课程 <el-icon><ArrowRight /></el-icon>
                  </el-button>
                </div>
              </el-card>
            </router-link>
          </el-col>
          <el-col :span="8">
            <router-link to="/community" class="feature-link">
              <el-card class="feature-card feature-community" shadow="hover">
                <div class="feature-icon">💬</div>
                <h3>学习社区</h3>
                <p class="feature-desc">28 个热门讨论帖</p>
                <p class="feature-detail">学员交流讨论，经验分享互助</p>
                <div class="feature-stats">
                  <div class="stat">
                    <span class="stat-value">28</span>
                    <span class="stat-label">帖子</span>
                  </div>
                  <div class="stat">
                    <span class="stat-value">178</span>
                    <span class="stat-label">评论</span>
                  </div>
                  <div class="stat">
                    <span class="stat-value">500+</span>
                    <span class="stat-label">用户</span>
                  </div>
                </div>
                <div class="feature-action">
                  <el-button type="primary" round size="small">
                    加入社区 <el-icon><ArrowRight /></el-icon>
                  </el-button>
                </div>
              </el-card>
            </router-link>
          </el-col>
        </el-row>
      </section>

      <!-- Stats Section -->
      <section class="stats-section">
        <div class="section-title">
          <h2>平台数据</h2>
          <p>数万名学员的选择</p>
        </div>
        <el-row :gutter="20" class="stats-grid">
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon">👥</div>
              <div class="stat-value">7</div>
              <div class="stat-label">注册用户</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon">📚</div>
              <div class="stat-value">258</div>
              <div class="stat-label">题库题目</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon">🎬</div>
              <div class="stat-value">18</div>
              <div class="stat-label">精品课程</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon">💬</div>
              <div class="stat-value">28</div>
              <div class="stat-label">社区帖子</div>
            </div>
          </el-col>
        </el-row>
      </section>

      <!-- Quick Actions -->
      <section class="quick-actions">
        <div class="section-title">
          <h2>快速开始</h2>
          <p>选择适合你的学习方式</p>
        </div>
        <el-row :gutter="16">
          <el-col :span="6">
            <router-link to="/question-bank" class="action-card">
              <div class="action-icon">🎯</div>
              <div class="action-title">每日一题</div>
              <div class="action-desc">每天进步一点点</div>
            </router-link>
          </el-col>
          <el-col :span="6">
            <router-link to="/question-bank" class="action-card">
              <div class="action-icon">📊</div>
              <div class="action-title">专项练习</div>
              <div class="action-desc">针对薄弱点突破</div>
            </router-link>
          </el-col>
          <el-col :span="6">
            <router-link to="/courses" class="action-card">
              <div class="action-icon">🏆</div>
              <div class="action-title">认证课程</div>
              <div class="action-desc">获取专业证书</div>
            </router-link>
          </el-col>
          <el-col :span="6">
            <router-link to="/community" class="action-card">
              <div class="action-icon">🤝</div>
              <div class="action-title">学习交流</div>
              <div class="action-desc">与学员互动</div>
            </router-link>
          </el-col>
        </el-row>
      </section>
    </main>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-section">
          <h4>关于我们</h4>
          <p>专业在线培训平台，提供高质量的课程和题库</p>
        </div>
        <div class="footer-section">
          <h4>联系方式</h4>
          <p>邮箱：support@training.com</p>
          <p>电话：400-888-8888</p>
        </div>
        <div class="footer-section">
          <h4>关注我们</h4>
          <div class="social-links">
            <span class="social-icon">微信</span>
            <span class="social-icon">微博</span>
            <span class="social-icon">知乎</span>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <p>© 2026 培训平台 - 专业在线培训解决方案</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useUserStore } from '@/store/user'

const userStore = useUserStore()
</script>

<style scoped>
.home {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(180deg, #f5f7fa 0%, #fff 100%);
}

/* Header */
.header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 12px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
}

.logo-icon {
  font-size: 28px;
}

.nav {
  display: flex;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 8px;
  color: #606266;
  text-decoration: none;
  transition: all 0.3s;
}

.nav-item:hover {
  background: #ecf5ff;
  color: #409eff;
}

.nav-item.router-link-active {
  background: #409eff;
  color: white;
}

.auth {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 20px;
  background: #f5f7fa;
  color: #606266;
  text-decoration: none;
  transition: all 0.3s;
}

.user-link:hover {
  background: #ecf5ff;
  color: #409eff;
}

/* Hero Section */
.hero {
  position: relative;
  padding: 80px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  overflow: hidden;
}

.hero-content {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
  position: relative;
  z-index: 1;
}

.hero-title {
  font-size: 48px;
  margin-bottom: 16px;
  font-weight: bold;
}

.gradient-text {
  background: linear-gradient(90deg, #fff, #e0e7ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 20px;
  opacity: 0.9;
  margin-bottom: 32px;
}

.cta {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.hero-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.floating-card {
  position: absolute;
  font-size: 40px;
  opacity: 0.15;
  animation: float 6s ease-in-out infinite;
}

.c1 { top: 20%; left: 10%; animation-delay: 0s; }
.c2 { top: 60%; left: 15%; animation-delay: 1s; }
.c3 { top: 30%; right: 15%; animation-delay: 2s; }
.c4 { top: 70%; right: 10%; animation-delay: 3s; }

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

/* Features Section */
.features {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 20px;
}

.section-title {
  text-align: center;
  margin-bottom: 40px;
}

.section-title h2 {
  font-size: 32px;
  color: #303133;
  margin-bottom: 8px;
}

.section-title p {
  color: #909399;
  font-size: 16px;
}

.feature-link {
  display: block;
  text-decoration: none;
  color: inherit;
}

.feature-card {
  text-align: center;
  padding: 30px 20px;
  border-radius: 16px;
  transition: all 0.3s;
  height: 100%;
  border: 2px solid transparent;
}

.feature-card:hover {
  transform: translateY(-8px);
  border-color: #409eff;
}

.feature-question .feature-icon { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.feature-course .feature-icon { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
.feature-community .feature-icon { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }

.feature-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 20px;
  font-size: 40px;
  color: white;
}

.feature-card h3 {
  font-size: 22px;
  color: #303133;
  margin-bottom: 8px;
}

.feature-desc {
  color: #409eff;
  font-weight: bold;
  margin-bottom: 8px;
}

.feature-detail {
  color: #909399;
  font-size: 14px;
  margin-bottom: 20px;
}

.feature-stats {
  display: flex;
  justify-content: space-around;
  padding: 20px 0;
  border-top: 1px solid #f0f0f0;
  margin-bottom: 20px;
}

.stat {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
}

.stat-label {
  display: block;
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.feature-action {
  margin-top: 16px;
}

/* Stats Section */
.stats-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 60px 20px;
}

.stats-section .section-title h2,
.stats-section .section-title p {
  color: white;
}

.stats-grid {
  max-width: 1200px;
  margin: 0 auto;
}

.stat-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  padding: 30px 20px;
  border-radius: 16px;
  text-align: center;
  color: white;
  transition: all 0.3s;
}

.stat-card:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-4px);
}

.stat-card .stat-icon {
  font-size: 40px;
  margin-bottom: 12px;
}

.stat-card .stat-value {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 8px;
}

.stat-card .stat-label {
  font-size: 14px;
  opacity: 0.9;
}

/* Quick Actions */
.quick-actions {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 20px;
}

.action-card {
  display: block;
  background: white;
  padding: 30px 20px;
  border-radius: 16px;
  text-align: center;
  text-decoration: none;
  color: inherit;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  transition: all 0.3s;
  border: 2px solid transparent;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(64,158,255,0.2);
  border-color: #409eff;
}

.action-icon {
  font-size: 40px;
  margin-bottom: 12px;
}

.action-title {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 6px;
}

.action-desc {
  font-size: 14px;
  color: #909399;
}

/* Footer */
.footer {
  background: #2c3e50;
  color: white;
  padding: 40px 20px 20px;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
  margin-bottom: 30px;
}

.footer-section h4 {
  font-size: 18px;
  margin-bottom: 16px;
}

.footer-section p {
  color: rgba(255,255,255,0.7);
  line-height: 1.8;
}

.social-links {
  display: flex;
  gap: 12px;
}

.social-icon {
  padding: 8px 16px;
  background: rgba(255,255,255,0.1);
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.social-icon:hover {
  background: #409eff;
}

.footer-bottom {
  max-width: 1200px;
  margin: 0 auto;
  padding-top: 20px;
  border-top: 1px solid rgba(255,255,255,0.1);
  text-align: center;
  color: rgba(255,255,255,0.5);
}

/* Responsive */
@media (max-width: 768px) {
  /* Header */
  .header-content {
    flex-wrap: wrap;
    padding: 10px 15px;
  }
  
  .logo-icon {
    font-size: 24px;
  }
  
  .logo-text {
    font-size: 16px;
  }
  
  .nav {
    display: none;
  }
  
  .auth {
    margin-left: auto;
  }
  
  .auth .el-button {
    padding: 8px 12px;
    font-size: 13px;
  }
  
  /* Hero */
  .hero {
    padding: 40px 15px 60px;
  }
  
  .hero-title {
    font-size: 24px;
    line-height: 1.3;
  }
  
  .hero-subtitle {
    font-size: 14px;
    margin-bottom: 20px;
  }
  
  .cta {
    display: flex;
    flex-direction: column;
    gap: 12px;
    width: 100%;
  }
  
  .cta .el-button {
    width: 100%;
  }
  
  .hero-decoration {
    display: none;
  }
  
  /* Features */
  .features {
    padding: 30px 15px;
  }
  
  .section-title h2 {
    font-size: 20px;
  }
  
  .section-title p {
    font-size: 14px;
  }
  
  .el-row {
    margin-left: 0 !important;
    margin-right: 0 !important;
  }
  
  .el-col {
    margin-bottom: 15px;
    padding-left: 0 !important;
    padding-right: 0 !important;
  }
  
  .feature-link {
    display: block;
    width: 100%;
  }
  
  .feature-card {
    padding: 20px 15px;
    margin-bottom: 15px;
  }
  
  .feature-icon {
    font-size: 40px;
  }
  
  .feature-card h3 {
    font-size: 17px;
    margin: 12px 0 8px;
  }
  
  .feature-desc {
    font-size: 13px;
    margin-bottom: 6px;
  }
  
  .feature-detail {
    font-size: 12px;
    display: none;
  }
  
  .feature-stats {
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 12px;
  }
  
  .stat {
    min-width: 60px;
  }
  
  .stat-value {
    font-size: 20px;
  }
  
  .stat-label {
    font-size: 11px;
  }
  
  .feature-action {
    margin-top: 12px;
  }
  
  /* Stats Section */
  .stats-section {
    padding: 40px 15px;
  }
  
  .stats-grid {
    display: grid !important;
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 15px !important;
  }
  
  .stat-card {
    padding: 15px 10px;
  }
  
  .stat-card .stat-icon {
    font-size: 28px;
  }
  
  .stat-card .stat-value {
    font-size: 24px;
  }
  
  .stat-card .stat-label {
    font-size: 12px;
  }
  
  /* Quick Actions */
  .quick-actions {
    padding: 30px 15px;
  }
  
  .quick-actions .el-row {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  
  .action-card {
    padding: 20px 10px;
  }
  
  .action-icon {
    font-size: 32px;
  }
  
  .action-title {
    font-size: 14px;
    margin-bottom: 4px;
  }
  
  .action-desc {
    font-size: 11px;
  }
  
  /* Footer */
  .footer {
    padding: 30px 15px 20px;
  }
  
  .footer-content {
    grid-template-columns: 1fr;
    gap: 20px;
    text-align: center;
  }
  
  .footer-section h4 {
    font-size: 15px;
    margin-bottom: 10px;
  }
  
  .footer-section p {
    font-size: 13px;
    margin-bottom: 8px;
  }
  
  .social-links {
    justify-content: center;
    gap: 10px;
  }
  
  .social-icon {
    padding: 6px 12px;
    font-size: 13px;
  }
  
  .footer-bottom p {
    font-size: 12px;
    text-align: center;
  }
}

/* Small phones */
@media (max-width: 375px) {
  .hero-title {
    font-size: 20px;
  }
  
  .logo-text {
    font-size: 14px;
  }
  
  .feature-card h3 {
    font-size: 15px;
  }
  
  .quick-actions .el-row {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: 1fr !important;
  }
}
</style>
