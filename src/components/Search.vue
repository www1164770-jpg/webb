<template>
  <div class="search-container">
    <input
      type="text"
      v-model="searchKeyword"
      placeholder="搜索网站..."
      class="search-input"
      @keyup.enter="handleSearch"
    />
    <button class="search-button" @click="handleSearch">搜索</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['search'])
const searchKeyword = ref('')

const handleSearch = () => {
  emit('search', searchKeyword.value)
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
