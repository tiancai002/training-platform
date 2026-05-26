<template>
  <div class="courses-page">
    <!-- Hero Section -->
    <section class="courses-hero">
      <div class="hero-content">
        <div class="hero-icon">🎬</div>
        <h1>精品课程</h1>
        <p class="hero-subtitle">18 门精选课程 · 专业讲师授课 · 直播录播结合</p>
        <div class="hero-stats">
          <div class="hero-stat">
            <span class="stat-value">18</span>
            <span class="stat-label">课程</span>
          </div>
          <div class="hero-stat">
            <span class="stat-value">3000+</span>
            <span class="stat-label">学员</span>
          </div>
          <div class="hero-stat">
            <span class="stat-value">4.9</span>
            <span class="stat-label">评分</span>
          </div>
          <div class="hero-stat">
            <span class="stat-value">200h+</span>
            <span class="stat-label">时长</span>
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
            <span>筛选课程</span>
          </div>
          <el-form :inline="true">
            <el-form-item label="课程分类">
              <el-select v-model="filters.category" placeholder="全部" clearable @change="loadCourses" style="width: 160px">
                <el-option label="前端开发" value="frontend" />
                <el-option label="后端开发" value="backend" />
                <el-option label="人工智能" value="ai" />
                <el-option label="数据库" value="database" />
                <el-option label="DevOps" value="devops" />
              </el-select>
            </el-form-item>
            <el-form-item label="难度">
              <el-select v-model="filters.level" placeholder="全部" clearable @change="loadCourses" style="width: 140px">
                <el-option label="入门" value="beginner" />
                <el-option label="进阶" value="intermediate" />
                <el-option label="高级" value="advanced" />
              </el-select>
            </el-form-item>
            <el-form-item label="类型">
              <el-select v-model="filters.type" placeholder="全部" clearable @change="loadCourses" style="width: 140px">
                <el-option label="录播" value="recorded" />
                <el-option label="直播" value="live" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="loadCourses" :icon="Search">查询</el-button>
              <el-button @click="resetFilters" :icon="Refresh">重置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </div>
    </section>

    <!-- Course Grid -->
    <section class="courses-section">
      <div class="section-header">
        <h2>
          <el-icon><VideoCamera /></el-icon>
          全部课程
        </h2>
        <div class="section-actions">
          <span class="section-count">共 {{ courses.length }} 门课程</span>
          <el-radio-group v-model="sortBy" size="small" @change="sortCourses">
            <el-radio-button label="default">默认排序</el-radio-button>
            <el-radio-button label="price_asc">价格从低到高</el-radio-button>
            <el-radio-button label="price_desc">价格从高到低</el-radio-button>
            <el-radio-button label="popular">最受欢迎</el-radio-button>
          </el-radio-group>
        </div>
      </div>
      
      <el-row :gutter="24" v-loading="loading">
        <el-col :span="8" v-for="course in courses" :key="course.id">
          <div class="course-card-wrapper" @click="viewCourse(course)">
            <el-card class="course-card" shadow="hover">
              <div class="course-cover">
                <img :src="course.cover_url || defaultCover" :alt="course.title" />
                <div class="cover-overlay">
                  <el-button type="primary" size="small" round>
                    <el-icon><VideoPlay /></el-icon>
                    查看详情
                  </el-button>
                </div>
                <el-tag class="course-type-tag" :type="course.course_type === 'live' ? 'warning' : 'info'" size="small">
                  {{ course.course_type === 'live' ? '🔴 直播' : '📹 录播' }}
                </el-tag>
              </div>
              
              <div class="course-body">
                <div class="course-tags">
                  <el-tag v-for="tag in (course.tags || []).slice(0,3)" :key="tag" size="small" effect="plain">
                    {{ tag }}
                  </el-tag>
                </div>
                
                <h3 class="course-title">{{ course.title }}</h3>
                <p class="course-subtitle">{{ course.subtitle }}</p>
                
                <div class="course-info">
                  <div class="info-item">
                    <el-icon><Clock /></el-icon>
                    <span>{{ formatDuration(course.duration) }}</span>
                  </div>
                  <div class="info-item">
                    <el-icon><User /></el-icon>
                    <span>{{ course.enrolled_count || 0 }}人在学</span>
                  </div>
                </div>
              </div>
              
              <div class="course-footer">
                <div class="course-price">
                  <span class="price">¥{{ course.price }}</span>
                  <span class="original-price" v-if="course.original_price">¥{{ course.original_price }}</span>
                </div>
                <div class="course-rating">
                  <el-icon><Star /></el-icon>
                  <span>4.9</span>
                </div>
              </div>
            </el-card>
          </div>
        </el-col>
      </el-row>
    </section>

    <!-- Course Detail Dialog -->
    <el-dialog v-model="showDialog" title="课程详情" width="800px" class="course-dialog">
      <div v-if="selectedCourse" class="course-detail">
        <div class="detail-cover">
          <img :src="selectedCourse.cover_url || defaultCover" :alt="selectedCourse.title" />
          <div class="detail-cover-content">
            <h2>{{ selectedCourse.title }}</h2>
            <p>{{ selectedCourse.subtitle }}</p>
          </div>
        </div>
        
        <div class="detail-content">
          <div class="detail-tags">
            <el-tag v-for="tag in (selectedCourse.tags || [])" :key="tag" size="small">{{ tag }}</el-tag>
          </div>
          
          <div class="detail-grid">
            <div class="detail-item">
              <div class="item-icon">📹</div>
              <div class="item-content">
                <div class="item-label">课程类型</div>
                <div class="item-value">{{ selectedCourse.course_type === 'live' ? '直播课程' : '录播视频' }}</div>
              </div>
            </div>
            <div class="detail-item">
              <div class="item-icon">⏱️</div>
              <div class="item-content">
                <div class="item-label">学习时长</div>
                <div class="item-value">{{ formatDuration(selectedCourse.duration) }}</div>
              </div>
            </div>
            <div class="detail-item">
              <div class="item-icon">👥</div>
              <div class="item-content">
                <div class="item-label">学员人数</div>
                <div class="item-value">{{ selectedCourse.enrolled_count || 0 }}人</div>
              </div>
            </div>
            <div class="detail-item">
              <div class="item-icon">💰</div>
              <div class="item-content">
                <div class="item-label">课程价格</div>
                <div class="item-value">
                  <span class="price">¥{{ selectedCourse.price }}</span>
                  <span class="original-price" v-if="selectedCourse.original_price">¥{{ selectedCourse.original_price }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="detail-description">
            <h4>📖 课程介绍</h4>
            <p>{{ selectedCourse.description }}</p>
          </div>
        </div>
      </div>
      <template #footer>
        <el-button @click="showDialog = false">关闭</el-button>
        <el-button type="primary" @click="enrollCourse" round>
          立即报名 <el-icon><ArrowRight /></el-icon>
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  Filter, Search, Refresh, VideoCamera, VideoPlay, Clock, User, Star, ArrowRight 
} from '@element-plus/icons-vue'

const loading = ref(false)
const showDialog = ref(false)
const selectedCourse = ref(null)
const courses = ref([])
const sortBy = ref('default')

const defaultCover = 'https://picsum.photos/seed/course/400/225'

const filters = reactive({
  category: '',
  level: '',
  type: ''
})

const loadCourses = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams()
    params.append('page', '1')
    params.append('page_size', '20')
    if (filters.category) params.append('category', filters.category)
    if (filters.level) params.append('level', filters.level)
    if (filters.type) params.append('type', filters.type)
    
    const response = await fetch(`/api/course/list?${params.toString()}`)
    const data = await response.json()
    courses.value = Array.isArray(data) ? data : (data.items || [])
    sortCourses()
  } catch (error) {
    console.error('Failed to load courses:', error)
    ElMessage.error('加载课程失败')
  } finally {
    loading.value = false
  }
}

const sortCourses = () => {
  switch (sortBy.value) {
    case 'price_asc':
      courses.value.sort((a, b) => a.price - b.price)
      break
    case 'price_desc':
      courses.value.sort((a, b) => b.price - a.price)
      break
    case 'popular':
      courses.value.sort((a, b) => (b.enrolled_count || 0) - (a.enrolled_count || 0))
      break
    default:
      break
  }
}

const resetFilters = () => {
  filters.category = ''
  filters.level = ''
  filters.type = ''
  loadCourses()
}

const viewCourse = (course) => {
  selectedCourse.value = course
  showDialog.value = true
}

const enrollCourse = () => {
  ElMessage.success('报名成功！即将开始学习')
  showDialog.value = false
}

const formatDuration = (minutes) => {
  if (!minutes) return '未知'
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  return hours > 0 ? `${hours}小时${mins}分钟` : `${mins}分钟`
}

onMounted(() => {
  loadCourses()
})
</script>

<style scoped>
.courses-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #f5f7fa 0%, #fff 100%);
  padding-bottom: 40px;
}

/* Hero Section */
.courses-hero {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  padding: 60px 20px 80px;
  position: relative;
  overflow: hidden;
}

.courses-hero .hero-content {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
  color: white;
  position: relative;
  z-index: 1;
}

.courses-hero .hero-icon {
  font-size: 80px;
  margin-bottom: 20px;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.courses-hero h1 {
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

/* Courses Section */
.courses-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.section-header h2 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 24px;
  color: #303133;
}

.section-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.section-count {
  color: #909399;
  font-size: 14px;
}

/* Course Card */
.course-card-wrapper {
  margin-bottom: 24px;
  cursor: pointer;
}

.course-card {
  border-radius: 16px;
  transition: all 0.3s;
  height: 100%;
  border: 2px solid transparent;
  overflow: hidden;
}

.course-card-wrapper:hover .course-card {
  transform: translateY(-8px);
  border-color: #f093fb;
  box-shadow: 0 12px 32px rgba(240,147,251,0.25);
}

.course-cover {
  position: relative;
  margin: -15px -15px 0 -15px;
  overflow: hidden;
  height: 200px;
}

.course-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.course-card-wrapper:hover .course-cover img {
  transform: scale(1.1);
}

.cover-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.course-card-wrapper:hover .cover-overlay {
  opacity: 1;
}

.course-type-tag {
  position: absolute;
  top: 12px;
  right: 12px;
}

.course-body {
  padding: 20px;
}

.course-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.course-title {
  font-size: 18px;
  color: #303133;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.course-subtitle {
  font-size: 14px;
  color: #909399;
  margin-bottom: 16px;
}

.course-info {
  display: flex;
  gap: 16px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #606266;
}

.course-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  margin: 0 -15px -15px;
  background: #f5f7fa;
  border-top: 1px solid #e4e7ed;
}

.course-price {
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.price {
  font-size: 24px;
  font-weight: bold;
  color: #f56c6c;
}

.original-price {
  font-size: 14px;
  color: #909399;
  text-decoration: line-through;
}

.course-rating {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #f7ba2a;
  font-weight: bold;
}

/* Course Dialog */
.course-dialog :deep(.el-dialog__body) {
  padding: 0;
}

.course-detail {
  overflow: hidden;
}

.detail-cover {
  position: relative;
  height: 300px;
  overflow: hidden;
}

.detail-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.detail-cover-content {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 30px;
  background: linear-gradient(transparent, rgba(0,0,0,0.8));
  color: white;
}

.detail-cover-content h2 {
  font-size: 28px;
  margin-bottom: 8px;
}

.detail-cover-content p {
  opacity: 0.9;
}

.detail-content {
  padding: 30px;
}

.detail-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.detail-item {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 12px;
}

.item-icon {
  font-size: 32px;
}

.item-content {
  flex: 1;
}

.item-label {
  font-size: 13px;
  color: #909399;
  margin-bottom: 4px;
}

.item-value {
  font-size: 16px;
  color: #303133;
  font-weight: bold;
}

.item-value .price {
  color: #f56c6c;
}

.item-value .original-price {
  color: #909399;
  font-size: 14px;
  text-decoration: line-through;
  margin-left: 8px;
}

.detail-description {
  padding-top: 20px;
  border-top: 1px solid #e4e7ed;
}

.detail-description h4 {
  font-size: 18px;
  color: #303133;
  margin-bottom: 16px;
}

.detail-description p {
  line-height: 1.8;
  color: #606266;
}

/* Responsive */
@media (max-width: 768px) {
  .courses-hero h1 {
    font-size: 32px;
  }
  
  .hero-stats {
    flex-wrap: wrap;
    gap: 20px;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .section-actions {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>

/* Responsive */
@media (max-width: 768px) {
  .courses-page {
    padding: 0;
  }
  
  .courses-hero {
    padding: 40px 15px 60px;
  }
  
  .courses-hero h1 {
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
  
  .section-header {
    padding: 20px 15px;
  }
  
  .section-header h2 {
    font-size: 18px;
  }
  
  .filter-bar {
    flex-direction: column;
    gap: 12px;
    padding: 15px;
  }
  
  .course-filters {
    width: 100%;
  }
  
  .course-filters .el-input,
  .course-filters .el-select {
    width: 100%;
  }
  
  .course-grid {
    grid-template-columns: 1fr !important;
    gap: 15px !important;
    padding: 0 15px;
  }
  
  .course-card {
    padding: 15px;
  }
  
  .course-icon {
    font-size: 32px;
  }
  
  .course-card h3 {
    font-size: 16px;
  }
  
  .course-card p {
    font-size: 13px;
  }
  
  .course-meta {
    flex-wrap: wrap;
    font-size: 12px;
  }
  
  .course-footer {
    flex-direction: column;
    gap: 10px;
  }
  
  .course-footer .el-button {
    width: 100%;
  }
}

/* Small phones */
@media (max-width: 375px) {
  .courses-hero h1 {
    font-size: 20px;
  }
  
  .course-card h3 {
    font-size: 15px;
  }
}
