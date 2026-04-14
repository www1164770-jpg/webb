<template>
  <div class="app">
    <Navbar />
    <Search @search="handleSearch" />
    <div class="container">
      <Home />
    </div>
  </div>
</template>

<script setup>
import Navbar from './components/Navbar.vue'
import Search from './components/Search.vue'
import Home from './views/Home.vue'

// 处理搜索
const handleSearch = (keyword) => {
  // 这里可以通过事件总线或状态管理传递搜索关键词
  console.log('搜索关键词:', keyword)
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
}

.app {
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

@media (max-width: 768px) {
  .container {
    padding: 10px;
  }
}
</style>
