<template>
  <div class="practice-page">
    <!-- 答题模式 -->
    <div v-if="mode === 'practice'" class="practice-mode">
      <div class="header">
        <div class="progress">
          <span>第 {{ currentQuestionIndex + 1 }} / {{ questions.length }} 题</span>
          <el-progress :percentage="((currentQuestionIndex + 1) / questions.length * 100).toFixed(0)" :stroke-width="8" />
        </div>
        <el-button @click="exitPractice" size="small">退出</el-button>
      </div>

      <el-card v-if="currentQuestion" class="question-card">
        <div class="question-content">
          <div class="tags">
            <el-tag size="small">{{ currentQuestion.difficulty === 'easy' ? '简单' : currentQuestion.difficulty === 'medium' ? '中等' : '困难' }}</el-tag>
            <el-tag v-for="tag in currentQuestion.tags" :key="tag" size="small">{{ tag }}</el-tag>
          </div>
          <h3 class="question-text">{{ currentQuestion.content }}</h3>
        </div>

        <!-- 选项 -->
        <div v-if="currentQuestion.options" class="options">
          <div
            v-for="opt in currentQuestion.options"
            :key="opt.key"
            class="option-item"
            :class="{ 
              selected: userAnswer === opt.key,
              correct: submitted && opt.key === currentQuestion.answer,
              wrong: submitted && userAnswer === opt.key && opt.key !== currentQuestion.answer
            }"
            @click="selectAnswer(opt.key)"
          >
            <span class="option-key">{{ opt.key }}.</span>
            <span class="option-value">{{ opt.value }}</span>
          </div>
        </div>

        <!-- 提交按钮 -->
        <div class="actions" v-if="!submitted">
          <el-button type="primary" @click="submitAnswer" :disabled="!userAnswer" :loading="submitting">
            提交答案
          </el-button>
        </div>

        <!-- 结果 -->
        <div v-else class="result">
          <el-alert
            :title="isCorrect ? '✅ 回答正确！' : '❌ 回答错误'"
            :type="isCorrect ? 'success' : 'error'"
            :closable="false"
            show-icon
          />
          <div v-if="!isCorrect" class="correct-answer">
            <strong>正确答案：</strong>{{ currentQuestion.answer }}
          </div>
          <div v-if="currentQuestion.explanation" class="explanation">
            <strong>解析：</strong>{{ currentQuestion.explanation }}
          </div>
          <el-button type="primary" @click="nextQuestion" :disabled="isLastQuestion">
            {{ isLastQuestion ? '已完成' : '下一题' }}
          </el-button>
        </div>
      </el-card>

      <!-- 完成 -->
      <el-card v-if="showSummary" class="summary-card">
        <h3>🎉 练习完成！</h3>
        <div class="summary-stats">
          <div class="stat">
            <div class="stat-value">{{ total }}</div>
            <div class="stat-label">总题数</div>
          </div>
          <div class="stat">
            <div class="stat-value">{{ correctCount }}</div>
            <div class="stat-label">正确数</div>
          </div>
          <div class="stat">
            <div class="stat-value">{{ ((correctCount / total) * 100).toFixed(1) }}%</div>
            <div class="stat-label">正确率</div>
          </div>
        </div>
        <el-button type="primary" @click="exitPractice">返回</el-button>
      </el-card>
    </div>

    <!-- 每日一题模式 -->
    <div v-else-if="mode === 'daily'" class="daily-mode">
      <div class="daily-header">
        <h2>📅 每日一题</h2>
        <p>{{ dailyData.date }}</p>
      </div>

      <el-card v-if="dailyData.question" class="question-card">
        <div class="question-content">
          <h3 class="question-text">{{ dailyData.question.content }}</h3>
        </div>

        <div v-if="dailyData.question.options" class="options">
          <div
            v-for="opt in dailyData.question.options"
            :key="opt.key"
            class="option-item"
            :class="{ 
              selected: dailyAnswer === opt.key,
              correct: dailySubmitted && opt.key === dailyData.question.answer,
              wrong: dailySubmitted && dailyAnswer === opt.key && opt.key !== dailyData.question.answer
            }"
            @click="dailyAnswer = opt.key"
          >
            <span class="option-key">{{ opt.key }}.</span>
            <span class="option-value">{{ opt.value }}</span>
          </div>
        </div>

        <div class="actions" v-if="!dailySubmitted">
          <el-button type="primary" @click="submitDaily" :disabled="!dailyAnswer" :loading="submitting">
            提交答案
          </el-button>
        </div>

        <div v-else class="result">
          <el-alert
            :title="dailyCorrect ? '✅ 回答正确！' : '❌ 回答错误'"
            :type="dailyCorrect ? 'success' : 'error'"
            :closable="false"
            show-icon
          />
          <div v-if="!dailyCorrect" class="correct-answer">
            <strong>正确答案：</strong>{{ dailyData.question.answer }}
          </div>
          <div v-if="dailyData.question.explanation" class="explanation">
            <strong>解析：</strong>{{ dailyData.question.explanation }}
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { questionApi } from '@/api'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const mode = ref('practice') // 'practice' or 'daily'
const sessionId = ref('')
const questions = ref([])
const currentQuestionIndex = ref(0)
const userAnswer = ref('')
const submitted = ref(false)
const isCorrect = ref(false)
const submitting = ref(false)
const showSummary = ref(false)
const correctCount = ref(0)
const total = ref(0)

// 每日一题
const dailyData = ref({ date: '', question: null })
const dailyAnswer = ref('')
const dailySubmitted = ref(false)
const dailyCorrect = ref(false)

const currentQuestion = computed(() => {
  return questions.value[currentQuestionIndex.value] || null
})

const isLastQuestion = computed(() => {
  return currentQuestionIndex.value >= questions.value.length - 1
})

// 开始练习
const startPractice = async (bankId) => {
  try {
    const result = await questionApi.practice({
      bank_ids: [bankId],
      count: 10,
      mode: 'random'
    })
    sessionId.value = result.session_id
    questions.value = result.questions || []
    total.value = questions.value.length
    mode.value = 'practice'
  } catch (error) {
    ElMessage.error('加载题目失败：' + (error.message || '未知错误'))
  }
}

// 加载每日一题
const loadDaily = async () => {
  try {
    dailyData.value = await questionApi.getDaily({})
    mode.value = 'daily'
  } catch (error) {
    ElMessage.error('加载每日一题失败')
  }
}

// 选择答案
const selectAnswer = (key) => {
  if (submitted.value) return
  userAnswer.value = key
}

// 提交答案
const submitAnswer = async () => {
  if (!userAnswer.value) return
  
  submitting.value = true
  try {
    const result = await questionApi.submitPractice({
      session_id: sessionId.value,
      question_id: currentQuestion.value.id,
      user_answer: userAnswer.value
    })
    
    submitted.value = true
    isCorrect.value = result.is_correct
    if (result.is_correct) {
      correctCount.value++
      ElMessage.success('回答正确！✅')
    } else {
      ElMessage.error('回答错误')
    }
  } catch (error) {
    ElMessage.error('提交失败：' + (error.message || '未知错误'))
  } finally {
    submitting.value = false
  }
}

// 提交每日一题
const submitDaily = async () => {
  if (!dailyAnswer.value) return
  
  submitting.value = true
  try {
    const result = await questionApi.submitPractice({
      session_id: 'daily',
      question_id: dailyData.value.question.id,
      user_answer: dailyAnswer.value
    })
    
    dailySubmitted.value = true
    dailyCorrect.value = result.is_correct
    if (result.is_correct) {
      ElMessage.success('回答正确！✅')
    } else {
      ElMessage.error('回答错误')
    }
  } catch (error) {
    ElMessage.error('提交失败：' + (error.message || '未知错误'))
  } finally {
    submitting.value = false
  }
}

// 下一题
const nextQuestion = () => {
  if (isLastQuestion.value) {
    showSummary.value = true
    return
  }
  currentQuestionIndex.value++
  userAnswer.value = ''
  submitted.value = false
  isCorrect.value = false
}

// 退出练习
const exitPractice = () => {
  if (route.query.from === 'daily') {
    router.push('/question-bank')
  } else {
    router.push('/question-bank')
  }
}

onMounted(() => {
  if (route.query.bank_id) {
    startPractice(parseInt(route.query.bank_id))
  } else if (route.query.daily === '1') {
    loadDaily()
  } else {
    router.push('/question-bank')
  }
})
</script>

<style scoped>
.practice-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.progress {
  flex: 1;
  margin-right: 20px;
}

.question-card {
  margin-bottom: 20px;
}

.question-content {
  margin-bottom: 25px;
}

.tags {
  display: flex;
  gap: 8px;
  margin-bottom: 15px;
}

.question-text {
  font-size: 18px;
  line-height: 1.6;
  color: #333;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 25px;
}

.option-item {
  display: flex;
  align-items: flex-start;
  padding: 15px 20px;
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.option-item:hover {
  border-color: #409eff;
  background: #f5f7fa;
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
  margin-right: 10px;
  min-width: 25px;
}

.option-value {
  flex: 1;
  line-height: 1.5;
}

.actions {
  text-align: center;
}

.result {
  margin-top: 20px;
}

.correct-answer {
  margin: 15px 0;
  padding: 10px 15px;
  background: #fef0f0;
  border-radius: 4px;
  color: #f56c6c;
}

.explanation {
  margin: 15px 0;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 4px;
  line-height: 1.6;
}

.summary-card {
  text-align: center;
  padding: 40px 20px;
}

.summary-stats {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin: 30px 0;
}

.stat {
  text-align: center;
}

.stat-value {
  font-size: 36px;
  font-weight: bold;
  color: #409eff;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-top: 5px;
}

.daily-header {
  text-align: center;
  margin-bottom: 30px;
}

.daily-header h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 10px;
}

.daily-header p {
  color: #666;
}
</style>
