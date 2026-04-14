<template>
  <div class="search-container">
    <select v-model="currentEngine" class="engine-select">
      <option value="baidu">百度</option>
      <option value="google">谷歌</option>
      <option value="bing">必应</option>
    </select>
    
    <input
      type="text"
      v-model="searchKeyword"
      placeholder="输入关键词搜索..."
      class="search-input"
      @keyup.enter="handleSearch"
    />
    <button @click="handleSearch" class="search-btn">搜索</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const searchKeyword = ref('')
const currentEngine = ref('baidu') // 默认百度

// 引擎 URL 配置
const engines = {
  baidu: 'https://www.baidu.com/s?wd=',
  google: 'https://www.google.com/search?q=',
  bing: 'https://www.bing.com/search?q='
}

const handleSearch = () => {
  if (!searchKeyword.ref.trim()) return
  
  // 在新窗口打开对应引擎的搜索结果
  const url = engines[currentEngine.value] + encodeURIComponent(searchKeyword.value)
  window.open(url, '_blank')
}
</script>

<style scoped>
.search-container {
  max-width: 600px;
  margin: 20px auto;
  display: flex;
  gap: 10px;
}

.search-input {
  flex: 1;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 20px;
  font-size: 16px;
  outline: none;
  transition: border-color 0.3s;
}

.search-input:focus {
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.1);
}

.search-button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 20px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.search-button:hover {
  background-color: #45a049;
}

@media (max-width: 768px) {
  .search-container {
    margin: 10px;
  }
  
  .search-input {
    font-size: 14px;
  }
  
  .search-button {
    font-size: 14px;
    padding: 8px 16px;
  }
}
</style>
