<template>
  <div class="website-card" @click="openWebsite">
    <div class="website-icon">
      <img :src="faviconUrl" :alt="website.name" />
    </div>
    <h3 class="website-name">{{ website.name }}</h3>
    <p class="website-description">{{ website.description }}</p>
    <p class="website-url">{{ website.url }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  website: {
    type: Object,
    required: true
  }
})

// 生成favicon URL
const faviconUrl = computed(() => {
  // 提取域名
  const url = new URL(props.website.url)
  return `https://www.google.com/s2/favicons?domain=${url.hostname}&sz=64`
})

// 打开网站
const openWebsite = () => {
  window.open(props.website.url, '_blank')
}
</script>

<style scoped>
.website-card {
  background-color: white;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.website-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.website-icon {
  width: 64px;
  height: 64px;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.website-icon img {
  max-width: 100%;
  max-height: 100%;
  border-radius: 8px;
}

.website-name {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}

.website-description {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
  flex: 1;
}

.website-url {
  font-size: 12px;
  color: #999;
  word-break: break-all;
}

@media (max-width: 768px) {
  .website-card {
    padding: 10px;
  }
  
  .website-icon {
    width: 48px;
    height: 48px;
  }
  
  .website-name {
    font-size: 14px;
  }
  
  .website-description {
    font-size: 12px;
  }
  
  .website-url {
    font-size: 10px;
  }
}
</style>
