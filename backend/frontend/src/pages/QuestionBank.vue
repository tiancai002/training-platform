<template>
  <div class="question-bank-page">
    <!-- Hero Section -->
    <section class="qb-hero">
      <div class="hero-content">
        <div class="hero-icon">📝</div>
        <h1>智能题库</h1>
        <p class="hero-subtitle">9 个题库 · 258 道精选题目 · 智能错题本</p>
        <div class="hero-stats">
          <div class="hero-stat">
            <span class="stat-value">9</span>
            <span class="stat-label">题库</span>
          </div>
          <div class="hero-stat">
            <span class="stat-value">258</span>
            <span class="stat-label">题目</span>
          </div>
          <div class="hero-stat">
            <span class="stat-value">89%</span>
            <span class="stat-label">通过率</span>
          </div>
          <div class="hero-stat">
            <span class="stat-value">24h</span>
            <span class="stat-label">随时练习</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Filter Section -->
    <section class="filter-section">
      <div class="filter-container">
        <el-card class="filter-card" shadow="never">
          <div class="filter-header">
            <el-icon><Filter /></el-icon>
            <span>筛选条件</span>
          </div>
          <el-form :inline="true">
            <el-form-item label="证书类型">
              <el-select v-model="filters.certificate" placeholder="全部" clearable style="width: 180px">
                <el-option label="职业资格证书" value="professional" />
                <el-option label="技能证书" value="skill" />
                <el-option label="培训证书" value="training" />
              </el-select>
            </el-form-item>
            <el-form-item label="难度等级">
              <el-select v-model="filters.level" placeholder="全部" clearable style="width: 150px">
                <el-option label="基础级" value="basic" />
                <el-option label="进阶级" value="intermediate" />
                <el-option label="高级" value="advanced" />
                <el-option label="专家级" value="expert" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="loadBanks" :icon="Search">查询</el-button>
              <el-button @click="resetFilters" :icon="Refresh">重置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </div>
    </section>

    <!-- Question Banks Grid -->
    <section class="banks-section">
      <div class="section-header">
        <h2>
          <el-icon><Document /></el-icon>
          题库列表
        </h2>
        <span class="section-count">共 {{ banks.length }} 个题库</span>
      </div>
      
      <el-row :gutter="24" v-loading="loading">
        <el-col :span="8" v-for="(bank, index) in banks" :key="bank.id">
          <div class="bank-card-wrapper" @click="goToPractice(bank)">
            <el-card class="bank-card" shadow="hover">
              <div class="bank-header">
                <div class="bank-icon" :style="getIconStyle(index)">
                  {{ getIconByIndex(index) }}
                </div>
                <el-tag :type="getLevelType(bank.certificate?.level)" size="small" effect="plain">
                  {{ getLevelText(bank.certificate?.level) }}
                </el-tag>
              </div>
              
              <div class="bank-body">
                <h3 class="bank-title">{{ bank.name }}</h3>
                <p class="bank-desc">{{ bank.description || '暂无描述' }}</p>
                
                <div class="bank-stats">
                  <div class="bank-stat">
                    <el-icon><Document /></el-icon>
                    <span>{{ bank.total_questions }} 道题</span>
                  </div>
                  <div class="bank-stat">
                    <el-icon><TrendCharts /></el-icon>
                    <span>活跃度 {{ getActiveLevel(index) }}</span>
                  </div>
                </div>
              </div>
              
              <div class="bank-footer">
                <el-button type="primary" round size="small">
                  开始刷题 <el-icon><ArrowRight /></el-icon>
                </el-button>
              </div>
            </el-card>
          </div>
        </el-col>
      </el-row>
    </section>

    <!-- Daily Question Card -->
    <section class="daily-section">
      <div class="section-header">
        <h2>
          <el-icon><Calendar /></el-icon>
          每日一题
        </h2>
        <el-button @click="loadDaily" :icon="Refresh" circle size="small" />
      </div>
      
      <el-card class="daily-card" shadow="never" v-loading="!dailyQuestion">
        <div v-if="dailyQuestion" class="daily-content">
          <div class="daily-header">
            <div class="daily-meta">
              <el-tag type="warning" size="small">📅 {{ dailyQuestion.date || '今日' }}</el-tag>
              <span class="daily-source">{{ dailyQuestion.question?.tags?.[0] || '综合' }}</span>
            </div>
          </div>
          
          <div class="daily-question">
            <p class="question-text">{{ dailyQuestion.question?.content }}</p>
            
            <div class="question-options" v-if="dailyQuestion.question?.options">
              <div
                v-for="opt in dailyQuestion.question.options"
                :key="opt.key"
                class="option-item"
                :class="{ 
                  selected: dailyAnswer === opt.key,
                  correct: dailySubmitted && opt.key === dailyQuestion.question?.answer,
                  wrong: dailySubmitted && dailyAnswer === opt.key && opt.key !== dailyQuestion.question?.answer
                }"
                @click="selectDailyAnswer(opt.key)"
              >
                <span class="option-key">{{ opt.key }}.</span>
                <span class="option-value">{{ opt.value }}</span>
              </div>
            </div>
          </div>
          
          <div class="daily-actions" v-if="!dailySubmitted">
            <el-button type="primary" @click="submitDaily" :loading="submitting" round>
              提交答案
            </el-button>
          </div>
          
          <div class="daily-result" v-else>
            <el-alert
              :title="isCorrect ? '✅ 回答正确！' : '❌ 回答错误'"
              :type="isCorrect ? 'success' : 'error'"
              :closable="false"
              show-icon
            />
            <div v-if="!isCorrect" class="correct-answer">
              <strong>正确答案：</strong>{{ dailyQuestion.question?.answer }}
            </div>
            <div v-if="dailyQuestion.question?.explanation" class="explanation">
              <strong>💡 解析：</strong>{{ dailyQuestion.question.explanation }}
            </div>
          </div>
        </div>
      </el-card>
    </section>

    <!-- Practice Stats -->
    <section class="stats-section">
      <div class="section-header">
        <h2>
          <el-icon><TrendCharts /></el-icon>
          我的练习统计
        </h2>
      </div>
      
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-card stat-blue">
            <div class="stat-icon">📝</div>
            <div class="stat-value">{{ stats.total_questions || 0 }}</div>
            <div class="stat-label">累计刷题</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card stat-green">
            <div class="stat-icon">✅</div>
            <div class="stat-value">{{ stats.correct_count || 0 }}</div>
            <div class="stat-label">正确数量</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card stat-orange">
            <div class="stat-icon">📊</div>
            <div class="stat-value">{{ (stats.correct_rate || 0).toFixed(1) }}%</div>
            <div class="stat-label">正确率</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card stat-red">
            <div class="stat-icon">📖</div>
            <div class="stat-value">{{ stats.wrong_book_size || 0 }}</div>
            <div class="stat-label">错题本</div>
          </div>
        </el-col>
      </el-row>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Document, Filter, Search, Refresh, ArrowRight, Calendar, TrendCharts } from '@element-plus/icons-vue'
import { questionApi } from '@/api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loading = ref(false)
const banks = ref([])
const dailyQuestion = ref(null)
const dailyAnswer = ref('')
const dailySubmitted = ref(false)
const submitting = ref(false)
const isCorrect = ref(false)
const stats = ref({})

const filters = reactive({
  certificate: '',
  level: ''
})

const icons = ['📚', '💻', '🔧', '📊', '🎯', '⭐', '🚀', '💡', '🏆']

const getIconByIndex = (index) => icons[index % icons.length]

const getIconStyle = (index) => {
  const colors = [
    'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
  ]
  return { background: colors[index % colors.length] }
}

const getActiveLevel = (index) => {
  const levels = ['🔥 高', '⭐ 中', '💎 新']
  return levels[index % levels.length]
}

const getLevelText = (level) => {
  const levelMap = {
    'basic': '基础级',
    'intermediate': '进阶级',
    'advanced': '高级',
    'expert': '专家级'
  }
  return levelMap[level] || '基础级'
}

const getLevelType = (level) => {
  const typeMap = {
    'basic': 'info',
    'intermediate': 'warning',
    'advanced': 'danger',
    'expert': ''
  }
  return typeMap[level] || 'info'
}

const loadBanks = async () => {
  loading.value = true
  try {
    const params = {}
    if (filters.certificate) params.certificate_type = filters.certificate
    if (filters.level) params.level = filters.level
    banks.value = await questionApi.getBanks(params)
  } catch (error) {
    console.error('Failed to load banks:', error)
    ElMessage.error('加载题库失败')
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  filters.certificate = ''
  filters.level = ''
  loadBanks()
}

const loadDaily = async () => {
  try {
    dailyQuestion.value = await questionApi.getDaily({})
    dailyAnswer.value = ''
    dailySubmitted.value = false
  } catch (error) {
    console.error('Failed to load daily question:', error)
  }
}

const selectDailyAnswer = (key) => {
  if (dailySubmitted.value) return
  dailyAnswer.value = key
}

const submitDaily = async () => {
  if (!dailyAnswer.value) {
    ElMessage.warning('请选择答案')
    return
  }
  
  submitting.value = true
  try {
    const result = await questionApi.submitPractice({
      session_id: 'daily',
      question_id: dailyQuestion.value.question.id,
      user_answer: dailyAnswer.value
    })
    
    dailySubmitted.value = true
    isCorrect.value = result.is_correct
    if (result.is_correct) {
      ElMessage.success('回答正确！🎉')
    } else {
      ElMessage.error('回答错误')
    }
  } catch (error) {
    console.error('Failed to submit:', error)
    ElMessage.error('提交失败')
  } finally {
    submitting.value = false
  }
}

const loadStats = async () => {
  try {
    stats.value = await questionApi.getStats()
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
}

const goToPractice = (bank) => {
  router.push({
    path: '/practice',
    query: { bank_id: bank.id }
  })
}

onMounted(() => {
  loadBanks()
  loadDaily()
  loadStats()
})
</script>

<style scoped>
.question-bank-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #f5f7fa 0%, #fff 100%);
  padding-bottom: 40px;
}

/* Hero Section */
.qb-hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 60px 20px 80px;
  position: relative;
  overflow: hidden;
}

.hero-content {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
  color: white;
  position: relative;
  z-index: 1;
}

.hero-icon {
  font-size: 80px;
  margin-bottom: 20px;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.qb-hero h1 {
  font-size: 48px;
  margin-bottom: 12px;
  font-weight: bold;
}

.hero-subtitle {
  font-size: 18px;
  opacity: 0.9;
  margin-bottom: 32px;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 40px;
}

.hero-stat {
  text-align: center;
}

.hero-stat .stat-value {
  display: block;
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 4px;
}

.hero-stat .stat-label {
  display: block;
  font-size: 14px;
  opacity: 0.8;
}

/* Filter Section */
.filter-section {
  max-width: 1200px;
  margin: -40px auto 40px;
  padding: 0 20px;
  position: relative;
  z-index: 10;
}

.filter-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.filter-card {
  border: none;
}

.filter-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  color: #303133;
  font-weight: bold;
  font-size: 16px;
}

/* Banks Section */
.banks-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-header h2 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 24px;
  color: #303133;
}

.section-count {
  color: #909399;
  font-size: 14px;
}

/* Bank Card */
.bank-card-wrapper {
  margin-bottom: 24px;
  cursor: pointer;
}

.bank-card {
  border-radius: 16px;
  transition: all 0.3s;
  height: 100%;
  border: 2px solid transparent;
}

.bank-card-wrapper:hover .bank-card {
  transform: translateY(-8px);
  border-color: #409eff;
  box-shadow: 0 12px 32px rgba(64,158,255,0.2);
}

.bank-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.bank-icon {
  width: 60px;
  height: 60px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  color: white;
}

.bank-title {
  font-size: 18px;
  color: #303133;
  margin-bottom: 8px;
}

.bank-desc {
  font-size: 14px;
  color: #909399;
  margin-bottom: 16px;
  line-height: 1.6;
}

.bank-stats {
  display: flex;
  gap: 16px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.bank-stat {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #606266;
}

.bank-footer {
  margin-top: 16px;
  text-align: center;
}

/* Daily Section */
.daily-section {
  max-width: 1200px;
  margin: 0 auto 40px;
  padding: 0 20px;
}

.daily-card {
  border-radius: 16px;
}

.daily-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.daily-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.daily-source {
  color: #909399;
  font-size: 14px;
}

.question-text {
  font-size: 16px;
  line-height: 1.8;
  color: #303133;
  margin-bottom: 24px;
}

.question-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.option-item {
  display: flex;
  padding: 16px 20px;
  border: 2px solid #e4e7ed;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.option-item:hover {
  border-color: #409eff;
  background: #ecf5ff;
}

.option-item.selected {
  border-color: #409eff;
  background: #ecf5ff;
}

.option-item.correct {
  border-color: #67c23a;
  background: #f0f9eb;
}

.option-item.wrong {
  border-color: #f56c6c;
  background: #fef0f0;
}

.option-key {
  font-weight: bold;
  margin-right: 12px;
  min-width: 25px;
  color: #409eff;
}

.option-value {
  flex: 1;
  line-height: 1.5;
}

.daily-actions {
  text-align: center;
}

.daily-result {
  margin-top: 20px;
}

.correct-answer {
  margin: 16px 0;
  padding: 12px 16px;
  background: #fef0f0;
  border-radius: 8px;
  color: #f56c6c;
}

.explanation {
  margin: 16px 0;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
  line-height: 1.8;
}

/* Stats Section */
.stats-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.stat-card {
  padding: 30px 20px;
  border-radius: 16px;
  text-align: center;
  color: white;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

.stat-blue { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.stat-green { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
.stat-orange { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }
.stat-red { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }

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
</style>

/* Responsive */
@media (max-width: 768px) {
  .qb-page {
    padding: 0;
  }
  
  .qb-hero {
    padding: 40px 15px 60px;
  }
  
  .qb-hero h1 {
    font-size: 24px;
  }
  
  .hero-subtitle {
    font-size: 14px;
  }
  
  .hero-stats {
    flex-wrap: wrap;
    gap: 20px;
  }
  
  .hero-stat .stat-value {
    font-size: 24px;
  }
  
  .filter-section {
    padding: 0 15px;
    margin-top: -30px;
  }
  
  .filter-container {
    padding: 15px;
  }
  
  .el-tabs__item {
    padding: 0 12px;
    font-size: 13px;
  }
  
  .bank-card {
    padding: 15px;
  }
  
  .bank-card h3 {
    font-size: 16px;
  }
  
  .bank-card p {
    font-size: 13px;
  }
  
  .bank-stats {
    flex-wrap: wrap;
  }
  
  .bank-stat {
    min-width: 70px;
  }
  
  .bank-stat-value {
    font-size: 18px;
  }
  
  .bank-stat-label {
    font-size: 11px;
  }
}
