<template>
  <div class="community-page">
    <h1>学习社区</h1>
    <p>帖子数：{{ posts.length }}</p>
    <p>分类数：{{ categories.length }}</p>
    <div v-if="loading">加载中...</div>
    <div v-else-if="error" style="color: red">{{ error }}</div>
    <div v-else>
      <div v-for="post in posts" :key="post.id" class="post-card" @click="viewPost(post)">
        <h3>{{ post.title }}</h3>
        <p>{{ post.content?.substring(0, 100) }}...</p>
        <div class="post-meta">
          <span>👤 {{ post.author?.nickname || '未知' }}</span>
          <span>👁 {{ post.view_count }} | ❤️ {{ post.like_count }} | 💬 {{ post.comment_count }}</span>
        </div>
      </div>
    </div>
    
    <!-- Post Detail Modal with Comments -->
    <div v-if="selectedPost" class="modal" @click="closeModal()">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ selectedPost.title }}</h2>
          <button class="close-btn" @click="closeModal()">✕</button>
        </div>
        
        <div class="modal-body">
          <!-- Post Info -->
          <div class="post-info">
            <span>👤 {{ selectedPost.author?.nickname || '未知' }}</span>
            <span>🕐 {{ formatDate(selectedPost.created_at) }}</span>
          </div>
          
          <!-- Post Content -->
          <div class="post-content">{{ selectedPost.content }}</div>
          
          <!-- Post Stats -->
          <div class="post-stats">
            <span>👁 {{ selectedPost.view_count }} 阅读</span>
            <span>❤️ {{ selectedPost.like_count }} 点赞</span>
            <span>💬 {{ selectedPost.comment_count }} 评论</span>
          </div>
          
          <!-- Comments Section -->
          <div class="comments-section">
            <h3>💬 评论交流 ({{ comments.length }})</h3>
            
            <!-- Comment Input -->
            <div class="comment-input">
              <textarea 
                v-model="newComment" 
                placeholder="写下你的评论..." 
                rows="3"
                maxlength="500"
              ></textarea>
              <div class="comment-input-footer">
                <span class="char-count">{{ newComment.length }}/500</span>
                <button @click="submitComment" :disabled="!newComment.trim() || submitting">
                  {{ submitting ? '发送中...' : '发表评论' }}
                </button>
              </div>
            </div>
            
            <!-- Comments List -->
            <div class="comments-list">
              <div v-for="comment in comments" :key="comment.id" class="comment-item">
                <div class="comment-avatar">👤</div>
                <div class="comment-body">
                  <div class="comment-header">
                    <span class="comment-author">{{ comment.author?.nickname || '未知用户' }}</span>
                    <span class="comment-time">{{ formatDate(comment.created_at) }}</span>
                  </div>
                  <div class="comment-content">{{ comment.content }}</div>
                </div>
              </div>
              <div v-if="comments.length === 0" class="no-comments">
                暂无评论，快来抢沙发吧！
              </div>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="closeModal()">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { communityApi } from '@/api'

const posts = ref([])
const categories = ref([])
const loading = ref(true)
const error = ref(null)
const selectedPost = ref(null)
const comments = ref([])
const newComment = ref('')
const submitting = ref(false)

const viewPost = async (post) => {
  selectedPost.value = post
  // Load comments
  try {
    const result = await communityApi.getPost(post.id)
    comments.value = result.comments || []
  } catch (e) {
    console.error('Failed to load comments:', e)
    comments.value = []
  }
}

const closeModal = () => {
  selectedPost.value = null
  comments.value = []
  newComment.value = ''
}

const submitComment = async () => {
  if (!newComment.value.trim()) return
  
  submitting.value = true
  try {
    await communityApi.addComment(selectedPost.value.id, {
      content: newComment.value.trim()
    })
    
    // Reload comments
    const result = await communityApi.getPost(selectedPost.value.id)
    comments.value = result.comments || []
    
    // Clear input
    newComment.value = ''
    
    // Update post comment count
    selectedPost.value.comment_count = (selectedPost.value.comment_count || 0) + 1
  } catch (e) {
    alert('评论失败：' + e.message)
  } finally {
    submitting.value = false
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return Math.floor(diff / 60000) + '分钟前'
  if (diff < 86400000) return Math.floor(diff / 3600000) + '小时前'
  if (diff < 604800000) return Math.floor(diff / 86400000) + '天前'
  
  return date.toLocaleDateString('zh-CN')
}

onMounted(async () => {
  try {
    categories.value = await communityApi.getCategories()
    const result = await communityApi.getPosts({ page: 1, page_size: 50 })
    posts.value = result.items || []
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.community-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.post-card {
  background: #fff;
  padding: 20px;
  margin: 15px 0;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: all 0.3s;
}

.post-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

.post-meta {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
  font-size: 13px;
  color: #909399;
}

/* Modal */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: #fff;
  border-radius: 16px;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e4e7ed;
}

.modal-header h2 {
  margin: 0;
  font-size: 22px;
  color: #303133;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  color: #909399;
  cursor: pointer;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.close-btn:hover {
  background: #f5f7fa;
}

.modal-body {
  padding: 24px;
  flex: 1;
  overflow-y: auto;
}

.post-info {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
  font-size: 14px;
  color: #909399;
}

.post-content {
  font-size: 15px;
  line-height: 1.8;
  color: #606266;
  margin-bottom: 20px;
  white-space: pre-wrap;
}

.post-stats {
  display: flex;
  gap: 20px;
  padding: 12px 16px;
  background: #f5f7fa;
  border-radius: 8px;
  font-size: 14px;
  color: #606266;
  margin-bottom: 24px;
}

/* Comments Section */
.comments-section {
  border-top: 1px solid #e4e7ed;
  padding-top: 20px;
}

.comments-section h3 {
  margin: 0 0 16px 0;
  font-size: 18px;
  color: #303133;
}

.comment-input {
  margin-bottom: 24px;
}

.comment-input textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  resize: vertical;
  font-size: 14px;
  font-family: inherit;
  transition: border-color 0.3s;
}

.comment-input textarea:focus {
  outline: none;
  border-color: #4facfe;
}

.comment-input-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}

.char-count {
  font-size: 13px;
  color: #909399;
}

.comment-input-footer button {
  padding: 8px 20px;
  background: #4facfe;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.3s;
}

.comment-input-footer button:hover:not(:disabled) {
  background: #00f2fe;
}

.comment-input-footer button:disabled {
  background: #c0c4cc;
  cursor: not-allowed;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment-item {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 12px;
}

.comment-avatar {
  font-size: 32px;
  flex-shrink: 0;
}

.comment-body {
  flex: 1;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.comment-author {
  font-weight: 600;
  color: #303133;
}

.comment-time {
  font-size: 13px;
  color: #909399;
}

.comment-content {
  font-size: 14px;
  line-height: 1.6;
  color: #606266;
  white-space: pre-wrap;
}

.no-comments {
  text-align: center;
  padding: 40px 20px;
  color: #909399;
  font-size: 14px;
}

.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid #e4e7ed;
  display: flex;
  justify-content: flex-end;
}

.modal-footer button {
  padding: 10px 24px;
  background: #4facfe;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.modal-footer button:hover {
  background: #00f2fe;
}

@media (max-width: 768px) {
  .community-page {
    padding: 15px;
  }
  
  .community-page h1 {
    font-size: 24px;
  }
  
  .community-page p {
    font-size: 14px;
  }
  
  .post-card {
    padding: 15px;
  }
  
  .post-card h3 {
    font-size: 16px;
  }
  
  .post-card p {
    font-size: 13px;
  }
  
  .post-meta {
    flex-direction: column;
    gap: 8px;
    font-size: 12px;
  }
  
  .modal {
    padding: 10px;
  }
  
  .modal-content {
    max-height: 95vh;
    border-radius: 12px;
  }
  
  .modal-header {
    padding: 15px;
  }
  
  .modal-header h2 {
    font-size: 18px;
  }
  
  .modal-body {
    padding: 15px;
  }
  
  .post-info {
    flex-direction: column;
    gap: 8px;
    font-size: 13px;
  }
  
  .post-content {
    font-size: 14px;
    line-height: 1.6;
  }
  
  .post-stats {
    flex-wrap: wrap;
    gap: 12px;
    font-size: 13px;
    padding: 10px;
  }
  
  .comments-section h3 {
    font-size: 16px;
  }
  
  .comment-input textarea {
    font-size: 14px;
    padding: 10px;
  }
  
  .comment-input-footer button {
    padding: 8px 16px;
    font-size: 13px;
  }
  
  .comment-item {
    flex-direction: column;
    padding: 12px;
  }
  
  .comment-avatar {
    font-size: 24px;
  }
  
  .comment-header {
    flex-direction: column;
    gap: 4px;
  }
  
  .comment-author {
    font-size: 14px;
  }
  
  .comment-time {
    font-size: 12px;
  }
  
  .comment-content {
    font-size: 13px;
  }
  
  .modal-footer {
    padding: 12px 15px;
  }
  
  .modal-footer button {
    width: 100%;
    padding: 12px;
  }
}

/* Small phones */
@media (max-width: 375px) {
  .community-page h1 {
    font-size: 20px;
  }
  
  .post-card h3 {
    font-size: 15px;
  }
  
  .modal-header h2 {
    font-size: 16px;
  }
}
</style>
