<template>
  <div class="home">
    <CategoryList
      v-for="category in categories"
      :key="category.id"
      :category="category"
      :websites="getWebsitesByCategory(category.id)"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import CategoryList from '../components/CategoryList.vue'

const categories = ref([])
const websites = ref([])

// 初始化数据
onMounted(async () => {
  await fetchCategories()
  await fetchWebsites()
})

// 获取分类
const fetchCategories = async () => {
  try {
    const response = await axios.get('/api/categories')
    categories.value = response.data
  } catch (error) {
    console.error('获取分类失败:', error)
  }
}

// 获取网站
const fetchWebsites = async () => {
  try {
    const response = await axios.get('/api/websites')
    websites.value = response.data.websites
  } catch (error) {
    console.error('获取网站失败:', error)
  }
}

// 根据分类获取网站
const getWebsitesByCategory = (categoryId) => {
  return websites.value.filter(website => website.category_id === categoryId)
}
</script>

<style scoped>
.home {
  margin-top: 20px;
}
</style>
