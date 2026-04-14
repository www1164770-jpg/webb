<template>
  <div class="category-list">
    <h2 class="category-title">{{ category.name }}</h2>
    <div class="websites-grid">
      <WebsiteCard
        v-for="website in websites"
        :key="website.id"
        :website="website"
      />
    </div>
  </div>
</template>

<script setup>
import WebsiteCard from './WebsiteCard.vue'

const props = defineProps({
  category: {
    type: Object,
    required: true
  },
  websites: {
    type: Array,
    required: true
  }
})
</script>

<style scoped>
.category-list {
  margin-bottom: 30px;
}

.category-title {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: #333;
  border-left: 4px solid #4CAF50;
  padding-left: 10px;
}

.websites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

@media (max-width: 768px) {
  .websites-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 10px;
  }
  
  .category-title {
    font-size: 1.2rem;
  }
}
</style>
