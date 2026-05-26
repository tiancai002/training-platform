<template>
  <div class="test-page">
    <h1>社区测试页面</h1>
    <p>如果看到这个页面，说明 Vue 路由正常</p>
    <p>帖子数：{{ posts.length }}</p>
    <p>分类数：{{ categories.length }}</p>
    <div v-for="post in posts" :key="post.id" class="post-item">
      <h3>{{ post.title }}</h3>
      <p>{{ post.content?.substring(0, 50) }}...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { communityApi } from '@/api'

const posts = ref([])
const categories = ref([])

onMounted(async () => {
  console.log('Test page mounted')
  try {
    categories.value = await communityApi.getCategories()
    console.log('Categories loaded:', categories.value.length)
    
    const result = await communityApi.getPosts({ page: 1, page_size: 10 })
    posts.value = result.items || []
    console.log('Posts loaded:', posts.value.length)
  } catch (error) {
    console.error('Failed to load:', error)
  }
})
</script>

<style scoped>
.test-page {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}
.post-item {
  background: #fff;
  padding: 15px;
  margin: 10px 0;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
</style>
