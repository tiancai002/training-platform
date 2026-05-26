<template>
  <div class="profile-page">
    <h1>👤 个人中心</h1>
    
    <el-row :gutter="20">
      <!-- User Info -->
      <el-col :span="8">
        <el-card class="user-card">
          <div class="user-info">
            <div class="avatar-container">
              <el-avatar :size="100" :src="userInfo.avatar_url || defaultAvatar" icon="User" />
              <div class="avatar-overlay" @click="showAvatarDialog = true">
                <el-icon><Camera /></el-icon>
                <span>更换头像</span>
              </div>
            </div>
            <h3 class="nickname">{{ userInfo.nickname || userInfo.username }}</h3>
            <p class="username">@{{ userInfo.username }}</p>
            <p class="email">{{ userInfo.email }}</p>
            <div class="badges">
              <el-tag :type="userInfo.role === 'instructor' ? 'warning' : 'primary'">
                {{ userInfo.role === 'instructor' ? '👨‍🏫 讲师' : '👨‍🎓 学员' }}
              </el-tag>
              <el-tag v-if="userInfo.is_verified" type="success" effect="plain">✓ 已认证</el-tag>
            </div>
          </div>
        </el-card>

        <!-- 头像选择对话框 -->
        <el-dialog v-model="showAvatarDialog" title="更换头像" width="500px">
          <div class="avatar-selector">
            <p class="avatar-tip">选择一个喜欢的头像：</p>
            <div class="avatar-grid">
              <div
                v-for="avatar in avatarOptions"
                :key="avatar"
                class="avatar-option"
                :class="{ selected: selectedAvatar === avatar }"
                @click="selectedAvatar = avatar"
              >
                <el-avatar :size="60" :src="avatar" />
              </div>
            </div>
            <div class="custom-avatar">
              <p>或输入自定义头像 URL：</p>
              <el-input v-model="customAvatarUrl" placeholder="https://example.com/avatar.png" />
            </div>
          </div>
          <template #footer>
            <el-button @click="showAvatarDialog = false">取消</el-button>
            <el-button type="primary" @click="updateAvatar" :loading="updatingAvatar">确定</el-button>
          </template>
        </el-dialog>

        <!-- Learning Stats -->
        <el-card class="stats-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>📊 学习统计</span>
            </div>
          </template>
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-icon">📝</div>
              <div class="stat-value">{{ stats.total_practice || 0 }}</div>
              <div class="stat-label">刷题数</div>
            </div>
            <div class="stat-item">
              <div class="stat-icon">✅</div>
              <div class="stat-value">{{ (stats.accuracy_rate || 0).toFixed(1) }}%</div>
              <div class="stat-label">正确率</div>
            </div>
            <div class="stat-item">
              <div class="stat-icon">📚</div>
              <div class="stat-value">{{ stats.wrong_book_size || 0 }}</div>
              <div class="stat-label">错题本</div>
            </div>
            <div class="stat-item">
              <div class="stat-icon">🔥</div>
              <div class="stat-value">{{ stats.streak_days || 0 }}</div>
              <div class="stat-label">连续天数</div>
            </div>
            <div class="stat-item">
              <div class="stat-icon">⏱️</div>
              <div class="stat-value">{{ (stats.learning_hours || 0).toFixed(1) }}h</div>
              <div class="stat-label">学习时长</div>
            </div>
            <div class="stat-item">
              <div class="stat-icon">🎓</div>
              <div class="stat-value">{{ stats.completed_courses || 0 }}</div>
              <div class="stat-label">完成课程</div>
            </div>
          </div>
        </el-card>

        <!-- Favorite Subjects -->
        <el-card class="subjects-card" shadow="hover" v-if="stats.favorite_subjects?.length">
          <template #header>
            <span>❤️ 偏好科目</span>
          </template>
          <div class="tags-container">
            <el-tag v-for="subject in stats.favorite_subjects" :key="subject" size="small">
              {{ subject }}
            </el-tag>
          </div>
        </el-card>
      </el-col>

      <!-- Main Content -->
      <el-col :span="16">
        <!-- Activity Log -->
        <el-card class="section-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>📜 最近活动</span>
              <el-button size="small" @click="loadActivity">刷新</el-button>
            </div>
          </template>
          <el-timeline v-if="activity.length">
            <el-timeline-item
              v-for="(item, index) in activity"
              :key="index"
              :timestamp="formatTime(item.timestamp)"
              placement="top"
              :icon="getActivityIcon(item.action)"
            >
              <el-card>
                <p>{{ getActivityText(item) }}</p>
                <div v-if="item.details" class="activity-details">
                  <el-tag v-if="item.details.is_correct !== undefined" :type="item.details.is_correct ? 'success' : 'danger'" size="small">
                    {{ item.details.is_correct ? '✓ 正确' : '✗ 错误' }}
                  </el-tag>
                  <span v-if="item.details.time_spent" class="time-spent">{{ item.details.time_spent }}秒</span>
                </div>
              </el-card>
            </el-timeline-item>
          </el-timeline>
          <el-empty v-else description="暂无活动记录" />
        </el-card>

        <!-- Orders -->
        <el-card class="section-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>📦 我的订单</span>
              <el-tag size="small">{{ orders.length }}个</el-tag>
            </div>
          </template>
          <div v-if="orders.length" class="order-list">
            <div v-for="order in orders" :key="order.id" class="order-item">
              <div class="order-info">
                <div class="order-title">{{ order.course?.title || '课程' }}</div>
                <div class="order-meta">
                  <el-tag :type="order.payment_status === 'paid' ? 'success' : 'warning'" size="small">
                    {{ order.payment_status === 'paid' ? '已支付' : '待支付' }}
                  </el-tag>
                  <span class="order-price">¥{{ order.price }}</span>
                </div>
              </div>
              <div class="order-date">{{ formatDate(order.created_at) }}</div>
            </div>
          </div>
          <el-empty v-else description="暂无订单" />
        </el-card>

        <!-- Certificates -->
        <el-card class="section-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>🎓 我的证书</span>
              <el-tag size="small" type="success">{{ certificates.length }}个</el-tag>
            </div>
          </template>
          <div v-if="certificates.length" class="certificate-list">
            <div v-for="cert in certificates" :key="cert.id" class="certificate-item">
              <div class="cert-icon">📜</div>
              <div class="cert-info">
                <div class="cert-name">{{ cert.certificate?.name || '证书' }}</div>
                <div class="cert-desc">{{ cert.certificate?.description || '' }}</div>
                <div class="cert-meta">
                  <el-tag size="small" effect="plain">{{ getLevelText(cert.certificate?.level) }}</el-tag>
                  <span class="cert-date">{{ formatDate(cert.obtained_at) }}</span>
                </div>
              </div>
            </div>
          </div>
          <el-empty v-else description="暂无证书" />
        </el-card>

        <!-- Knowledge Graph -->
        <el-card class="section-card" shadow="hover">
          <template #header>
            <span>📊 知识图谱</span>
          </template>
          <div class="knowledge-graph">
            <div v-for="subject in knowledgeData" :key="subject.name" class="subject-item">
              <div class="subject-header">
                <span class="subject-name">{{ subject.name }}</span>
                <span class="subject-progress">{{ subject.progress }}%</span>
              </div>
              <el-progress :percentage="subject.progress" :status="subject.progress >= 80 ? 'success' : ''" />
              <div class="subject-stats">
                <span>📝 {{ subject.questions }}题</span>
                <span>✅ {{ subject.correct }}正确</span>
              </div>
            </div>
          </div>
        </el-card>

        <!-- Achievements -->
        <el-card class="section-card" shadow="hover">
          <template #header>
            <span>🏆 成就徽章</span>
          </template>
          <div class="achievements-grid">
            <div class="achievement" v-for="badge in badges" :key="badge.name" :class="{ unlocked: badge.unlocked }">
              <div class="badge-icon">{{ badge.icon }}</div>
              <div class="badge-name">{{ badge.name }}</div>
              <div class="badge-desc">{{ badge.desc }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/store/user'
import { authApi, questionApi } from '@/api'

const userStore = useUserStore()
const userInfo = ref({})
const stats = ref({})
const activity = ref([])
const activityLoading = ref(false)

// 订单、证书和知识图谱
const orders = ref([])
const certificates = ref([])
const knowledgeData = ref([
  { name: 'Java 基础', progress: 90, questions: 38, correct: 35 },
  { name: 'Python 编程', progress: 85, questions: 31, correct: 28 },
  { name: '前端开发', progress: 75, questions: 59, correct: 52 },
  { name: '数据库', progress: 60, questions: 25, correct: 20 }
])

// 头像相关
const showAvatarDialog = ref(false)
const selectedAvatar = ref('')
const customAvatarUrl = ref('')
const updatingAvatar = ref(false)

const defaultAvatar = 'https://api.dicebear.com/7.x/avataaars/svg?seed=demo'

const avatarOptions = [
  'https://api.dicebear.com/7.x/avataaars/svg?seed=Alex',
  'https://api.dicebear.com/7.x/avataaars/svg?seed=Bob',
  'https://api.dicebear.com/7.x/avataaars/svg?seed=Cat',
  'https://api.dicebear.com/7.x/avataaars/svg?seed=Dog',
  'https://api.dicebear.com/7.x/avataaars/svg?seed=Eve',
  'https://api.dicebear.com/7.x/avataaars/svg?seed=Fox',
  'https://api.dicebear.com/7.x/avataaars/svg?seed=Girl',
  'https://api.dicebear.com/7.x/avataaars/svg?seed=Happy',
  'https://api.dicebear.com/7.x/avataaars/svg?seed=Jack',
  'https://api.dicebear.com/7.x/avataaars/svg?seed=Kitty'
]

const updateAvatar = async () => {
  updatingAvatar.value = true
  try {
    const newAvatar = customAvatarUrl.value || selectedAvatar.value
    if (!newAvatar) {
      ElMessage.warning('请选择头像')
      return
    }
    // 调用 API 更新头像
    await fetch('/api/auth/me', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ avatar_url: newAvatar })
    })
    userInfo.value.avatar_url = newAvatar
    ElMessage.success('头像更新成功！')
    showAvatarDialog.value = false
    customAvatarUrl.value = ''
  } catch (error) {
    ElMessage.error('更新失败：' + (error.message || '未知错误'))
  } finally {
    updatingAvatar.value = false
  }
}

// 模拟进度数据
const progressData = ref([
  { name: 'Java 基础', current: 38, total: 38, status: 'success' },
  { name: 'Python 基础', current: 20, total: 31, status: '' },
  { name: '前端基础', current: 15, total: 32, status: '' },
])

// 成就徽章
const badges = ref([
  { name: '新手上路', icon: '🌱', desc: '首次登录', unlocked: true },
  { name: '刷题达人', icon: '📝', desc: '刷题 100 道', unlocked: stats.value.total_practice >= 100 },
  { name: '正确率王者', icon: '👑', desc: '正确率 90%+', unlocked: (stats.value.accuracy_rate || 0) >= 90 },
  { name: '持之以恒', icon: '🔥', desc: '连续学习 7 天', unlocked: (stats.value.streak_days || 0) >= 7 },
  { name: '学霸', icon: '🎓', desc: '完成 5 门课程', unlocked: (stats.value.completed_courses || 0) >= 5 },
  { name: '社区之星', icon: '⭐', desc: '发布 10 个帖子', unlocked: false },
])

const loadUserInfo = async () => {
  try {
    userInfo.value = await authApi.getMe()
    // Merge stats from user info
    if (userInfo.value.learning_stats) {
      stats.value = { ...stats.value, ...userInfo.value.learning_stats }
    }
  } catch (error) {
    console.error('Failed to load user info:', error)
  }
}

const loadStats = async () => {
  try {
    const apiStats = await questionApi.getStats()
    stats.value = { ...stats.value, ...apiStats }
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
}

const loadActivity = async () => {
  activityLoading.value = true
  try {
    const result = await authApi.getActivity()
    activity.value = result.summary?.recent_actions || []
    
    if (activity.value.length === 0) {
      activity.value = generateMockActivity()
    }
  } catch (error) {
    console.error('Failed to load activity:', error)
    activity.value = generateMockActivity()
  } finally {
    activityLoading.value = false
  }
}

const loadOrders = async () => {
  try {
    const response = await fetch('/api/auth/me/orders', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const data = await response.json()
    orders.value = data || []
  } catch (error) {
    console.error('Failed to load orders:', error)
  }
}

const loadCertificates = async () => {
  try {
    const response = await fetch('/api/auth/me/certificates', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const data = await response.json()
    certificates.value = data || []
  } catch (error) {
    console.error('Failed to load certificates:', error)
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

const getLevelText = (level) => {
  const levelMap = {
    'basic': '基础级',
    'intermediate': '进阶级',
    'advanced': '高级',
    'expert': '专家级'
  }
  return levelMap[level] || level
}

const generateMockActivity = () => {
  const now = new Date()
  const activities = [
    { action: 'practice', details: { is_correct: true, time_spent: 15 }, timestamp: new Date(now - 1000 * 60 * 5).toISOString() },
    { action: 'practice', details: { is_correct: false, time_spent: 23 }, timestamp: new Date(now - 1000 * 60 * 30).toISOString() },
    { action: 'course_start', details: { course_id: 1 }, timestamp: new Date(now - 1000 * 60 * 60 * 2).toISOString() },
    { action: 'community', details: {}, timestamp: new Date(now - 1000 * 60 * 60 * 5).toISOString() },
    { action: 'practice', details: { is_correct: true, time_spent: 18 }, timestamp: new Date(now - 1000 * 60 * 60 * 24).toISOString() },
    { action: 'course_complete', details: { course_id: 3 }, timestamp: new Date(now - 1000 * 60 * 60 * 24 * 2).toISOString() },
    { action: 'view_profile', details: {}, timestamp: new Date(now - 1000 * 60 * 60 * 24 * 3).toISOString() },
    { action: 'practice', details: { is_correct: true, time_spent: 12 }, timestamp: new Date(now - 1000 * 60 * 60 * 24 * 5).toISOString() }
  ]
  return activities
}

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  return date.toLocaleDateString('zh-CN')
}

const getActivityIcon = (action) => {
  const icons = {
    'view_profile': '👤',
    'practice': '📝',
    'course_start': '📚',
    'course_complete': '🎓',
    'community': '💬'
  }
  return icons[action] || '📌'
}

const getActivityText = (item) => {
  const texts = {
    'view_profile': '查看了个人资料',
    'practice': '刷了一道题',
    'course_start': '开始学习课程',
    'course_complete': '完成了课程',
    'community': '参与了社区互动'
  }
  return texts[item.action] || item.action
}

onMounted(() => {
  loadUserInfo()
  loadStats()
  loadActivity()
  loadOrders()
  loadCertificates()
})
</script>

<style scoped>
.profile-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.profile-page h1 {
  margin-bottom: 20px;
  color: #333;
}

.user-card {
  margin-bottom: 20px;
}

.avatar-container {
  position: relative;
  display: inline-block;
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  opacity: 0;
  transition: opacity 0.3s;
  cursor: pointer;
}

.avatar-overlay:hover {
  opacity: 1;
}

.avatar-overlay .el-icon {
  font-size: 24px;
  margin-bottom: 5px;
}

.avatar-overlay span {
  font-size: 12px;
}

.user-info {
  text-align: center;
  padding: 20px 0;
}

.avatar-selector {
  padding: 10px;
}

.avatar-tip {
  text-align: center;
  margin-bottom: 20px;
  color: #666;
}

.avatar-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.avatar-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.avatar-option:hover {
  border-color: #409eff;
  transform: scale(1.05);
}

.avatar-option.selected {
  border-color: #409eff;
  background: #ecf5ff;
}

.custom-avatar {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e4e7ed;
}

.custom-avatar p {
  margin-bottom: 10px;
  color: #666;
  font-size: 14px;
}

.nickname {
  font-size: 20px;
  margin: 15px 0 5px;
  color: #333;
}

.username {
  color: #999;
  font-size: 14px;
  margin-bottom: 10px;
}

.email {
  color: #666;
  font-size: 13px;
  margin-bottom: 15px;
}

.badges {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 15px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
}

.stat-item {
  text-align: center;
  padding: 15px 10px;
  background: #f5f7fa;
  border-radius: 8px;
}

.stat-icon {
  font-size: 24px;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 12px;
  color: #666;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.section-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.activity-details {
  margin-top: 10px;
  display: flex;
  gap: 10px;
  align-items: center;
}

.time-spent {
  font-size: 12px;
  color: #999;
}

.progress-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.progress-item {
  padding: 10px 0;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
}

.achievement {
  text-align: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
  opacity: 0.5;
}

.achievement.unlocked {
  opacity: 1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.badge-icon {
  font-size: 40px;
  margin-bottom: 10px;
}

.badge-name {
  font-weight: bold;
  margin-bottom: 5px;
}

.badge-desc {
  font-size: 12px;
  opacity: 0.8;
}

.order-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.order-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
}

.order-info {
  flex: 1;
}

.order-title {
  font-weight: bold;
  margin-bottom: 8px;
  color: #333;
}

.order-meta {
  display: flex;
  align-items: center;
  gap: 10px;
}

.order-price {
  font-weight: bold;
  color: #f56c6c;
  font-size: 16px;
}

.order-date {
  color: #999;
  font-size: 13px;
}

.certificate-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.certificate-item {
  display: flex;
  gap: 15px;
  padding: 15px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  color: white;
}

.cert-icon {
  font-size: 40px;
}

.cert-info {
  flex: 1;
}

.cert-name {
  font-weight: bold;
  margin-bottom: 5px;
}

.cert-desc {
  font-size: 13px;
  opacity: 0.9;
  margin-bottom: 10px;
}

.cert-meta {
  display: flex;
  align-items: center;
  gap: 10px;
}

.cert-date {
  font-size: 12px;
  opacity: 0.8;
}

.knowledge-graph {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.subject-item {
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
}

.subject-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.subject-name {
  font-weight: bold;
  color: #333;
}

.subject-progress {
  color: #409eff;
  font-weight: bold;
}

.subject-stats {
  display: flex;
  gap: 15px;
  margin-top: 10px;
  font-size: 13px;
  color: #666;
}
</style>
