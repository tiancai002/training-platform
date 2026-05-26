<template>
  <div class="wrong-book-page">
    <div class="page-header">
      <h1>错题本</h1>
      <p>查漏补缺，针对性练习</p>
    </div>

    <el-card>
      <div class="stats">
        <el-statistic title="错题总数" :value="wrongBook.length" />
        <el-statistic title="已掌握" :value="masteredCount" />
      </div>

      <el-divider />

      <div v-if="wrongBook.length === 0" class="empty">
        <el-empty description="太棒了！没有错题" />
      </div>

      <div v-else class="question-list">
        <div v-for="item in wrongBook" :key="item.id" class="question-item">
          <div class="question-content">
            <el-tag type="danger" size="small">错 {{ item.wrong_count }} 次</el-tag>
            <p>{{ item.question_content }}</p>
          </div>
          <div class="actions">
            <el-button size="small" @click="practiceQuestion(item)">练习</el-button>
            <el-button size="small" @click="removeQuestion(item)">移除</el-button>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { questionApi } from '@/api'
import { ElMessage } from 'element-plus'

const wrongBook = ref([])

const masteredCount = computed(() => {
  return wrongBook.value.filter(q => q.correct_count >= q.remove_threshold).length
})

const loadWrongBook = async () => {
  try {
    wrongBook.value = await questionApi.getWrongBook()
  } catch (error) {
    console.error('Failed to load wrong book:', error)
  }
}

const practiceQuestion = (item) => {
  // Navigate to practice with specific question
  ElMessage.info('开始练习该题目')
}

const removeQuestion = async (item) => {
  try {
    await questionApi.removeWrongBook(item.question_id)
    ElMessage.success('已移除')
    loadWrongBook()
  } catch (error) {
    console.error('Failed to remove:', error)
  }
}

onMounted(() => {
  loadWrongBook()
})
</script>

<style scoped>
.wrong-book-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h1 {
  font-size: 24px;
  color: #333;
  margin-bottom: 5px;
}

.stats {
  display: flex;
  gap: 40px;
  justify-content: center;
}

.question-list {
  margin-top: 20px;
}

.question-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.question-content {
  flex: 1;
  margin-right: 20px;
}

.question-content p {
  margin-top: 10px;
  line-height: 1.6;
}

.actions {
  display: flex;
  gap: 10px;
}
</style>
