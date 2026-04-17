<template>
  <div class="search-wrapper">
    <!-- 搜索框区域 -->
    <div class="search-container">
      <input
        type="text"
        v-model="searchKeyword"
        placeholder="输入关键词搜索..."
        class="search-input"
        @keyup.enter="handleSearch"
      />
      <button @click="handleSearch" class="search-btn">🔍 搜索</button>
    </div>

    <!-- 搜索引擎切换栏（毛玻璃背景） -->
    <div class="engine-switcher-wrapper">
      <div class="engine-switcher">
        <!-- 滑动指示条（倒三角 + 胶囊） -->
        <div
          class="indicator"
          :style="{ left: `${indicatorPosition}px` }"
        >
          <div class="indicator-triangle"></div>
          <div class="indicator-pill"></div>
        </div>

        <!-- 搜索引擎按钮组 -->
        <div class="engine-buttons">
          <button
            v-for="engine in engineList"
            :key="engine.id"
            :ref="el => { if (el) engineRefs[engine.id] = el }"
            class="engine-btn"
            :class="{ active: currentEngine === engine.id }"
            @click="selectEngine(engine.id)"
          >
            <!-- 引擎图标 -->
            <span class="engine-icon" :style="{ backgroundColor: engine.color }">
              {{ engine.icon }}
            </span>
            <!-- 引擎名称 -->
            <span class="engine-name">{{ engine.label }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, nextTick, onMounted } from 'vue'

// ============ 搜索相关 ============
const searchKeyword = ref('')

// ============ 搜索引擎配置 ============
const engineList = [
  {
    id: 'baidu',
    label: '百度',
    icon: '🔍',
    color: '#EE5C42',
    url: 'https://www.baidu.com/s?wd='
  },
  {
    id: 'google',
    label: '谷歌',
    icon: 'G',
    color: '#4285F4',
    url: 'https://www.google.com/search?q='
  },
  {
    id: 'bing',
    label: '必应',
    icon: 'Bing',
    color: '#108DE5',
    url: 'https://www.bing.com/search?q='
  }
]

// ============ 状态管理 ============
const currentEngine = ref('baidu')
const indicatorPosition = ref(0)
const engineRefs = reactive({})

// ============ 计算指示器位置 ============
const updateIndicatorPosition = async () => {
  await nextTick()
  const ref = engineRefs[currentEngine.value]
  if (ref) {
    const offsetLeft = ref.offsetLeft
    indicatorPosition.value = offsetLeft
  }
}

// ============ 选择搜索引擎 ============
const selectEngine = (engineId) => {
  currentEngine.value = engineId
  localStorage.setItem('selectedEngine', engineId)
  updateIndicatorPosition()
}

// ============ 执行搜索 ============
const handleSearch = () => {
  if (!searchKeyword.value.trim()) {
    alert('请输入搜索关键词')
    return
  }

  const engine = engineList.find(e => e.id === currentEngine.value)
  const searchUrl = engine.url + encodeURIComponent(searchKeyword.value.trim())
  
  window.open(searchUrl, '_blank', 'noopener,noreferrer')
  
  // 清空输入框
  searchKeyword.value = ''
}

// ============ 组件挂载 ============
onMounted(() => {
  // 从 localStorage 恢复上次选择的引擎
  const saved = localStorage.getItem('selectedEngine')
  if (saved && engineList.find(e => e.id === saved)) {
    currentEngine.value = saved
  }
  
  // 初始化指示器位置
  updateIndicatorPosition()
  
  // 监听窗口大小变化，重新计算位置
  window.addEventListener('resize', updateIndicatorPosition)
})
</script>

<style scoped>
/* ============ CSS 变量定义 ============ */
:root {
  --primary-color: #3B82F6;
  --primary-hover: #2563EB;
  --glass-bg: rgba(255, 255, 255, 0.7);
  --glass-border: rgba(255, 255, 255, 0.2);
  --text-primary: #1F2937;
  --text-secondary: #6B7280;
  --text-muted: #9CA3AF;
}

/* ============ 搜索包装器 ============ */
.search-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  padding: 2rem 1rem;
  width: 100%;
  max-width: 700px;
  margin: 0 auto;
}

/* ============ 搜索框容器 ============ */
.search-container {
  display: flex;
  gap: 0.75rem;
  width: 100%;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.search-container:focus-within {
  background: rgba(255, 255, 255, 0.95);
  border-color: var(--primary-color);
  box-shadow: 0 8px 32px 0 rgba(59, 130, 246, 0.2);
  transform: translateY(-2px);
}

/* ============ 搜索输入框 ============ */
.search-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: none;
  background: transparent;
  font-size: 1rem;
  color: var(--text-primary);
  outline: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.search-input::placeholder {
  color: var(--text-muted);
}

/* ============ 搜索按钮 ============ */
.search-btn {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-hover) 100%);
  color: white;
  border: none;
  border-radius: 0.75rem;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
  white-space: nowrap;
}

.search-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
}

.search-btn:active {
  transform: translateY(0);
}

/* ============ 搜索引擎切换栏（毛玻璃） ============ */
.engine-switcher-wrapper {
  width: 100%;
  padding: 1.5rem;
  background: rgba(248, 250, 252, 0.5);
  backdrop-filter: blur(20px);
  border-radius: 1.25rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.08);
  animation: slideUp 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.engine-switcher {
  position: relative;
  display: flex;
  justify-content: center;
  gap: 2rem;
}

/* ============ 滑动指示条 ============ */
.indicator {
  position: absolute;
  bottom: -40px;
  left: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  transition: left 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  pointer-events: none;
}

/* 倒三角形指示器 */
.indicator-triangle {
  width: 0;
  height: 0;
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-bottom: 8px solid var(--primary-color);
  animation: trianglePulse 0.6s ease-out forwards;
}

@keyframes trianglePulse {
  0% {
    opacity: 0;
    transform: scale(0) translateY(-10px);
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* 胶囊型背景指示器 */
.indicator-pill {
  width: 90px;
  height: 4px;
  background: linear-gradient(90deg, var(--primary-color), #60A5FA);
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
  animation: pillExpand 0.4s ease-out forwards;
}

@keyframes pillExpand {
  from {
    width: 0;
    opacity: 0;
  }
  to {
    width: 90px;
    opacity: 1;
  }
}

/* ============ 引擎按钮组 ============ */
.engine-buttons {
  display: flex;
  gap: 2rem;
  justify-content: center;
  flex-wrap: wrap;
  z-index: 1;
}

/* ============ 单个引擎按钮 ============ */
.engine-btn {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  color: var(--text-secondary);
  font-weight: 500;
  font-size: 0.95rem;
  border-radius: 0.875rem;
}

.engine-btn:hover {
  color: var(--text-primary);
  transform: scale(1.08) translateY(-4px);
}

.engine-btn:hover .engine-icon {
  transform: scale(1.15) rotate(5deg);
  box-shadow: 0 8px 16px rgba(59, 130, 246, 0.25);
}

/* 选中态 */
.engine-btn.active {
  color: var(--primary-color);
  font-weight: 700;
  text-shadow: 0 0 20px rgba(59, 130, 246, 0.1);
}

.engine-btn.active .engine-icon {
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
  transform: scale(1.1);
}

/* ============ 引擎图标 ============ */
.engine-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  color: white;
  font-weight: bold;
  font-size: 1.25rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background: var(--primary-color);
}

/* ============ 引擎名称 ============ */
.engine-name {
  display: inline-block;
  transition: all 0.3s ease;
  min-width: 50px;
  text-align: center;
}

/* ============ 响应式设计 ============ */
@media (max-width: 768px) {
  .search-wrapper {
    gap: 1.5rem;
    padding: 1rem;
  }

  .engine-switcher-wrapper {
    padding: 1rem;
  }

  .engine-switcher {
    gap: 1.5rem;
  }

  .engine-btn {
    padding: 0.75rem;
  }

  .engine-icon {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }

  .engine-name {
    font-size: 0.85rem;
  }

  .indicator {
    bottom: -32px;
  }

  .indicator-pill {
    width: 70px;
  }
}

@media (max-width: 480px) {
  .search-wrapper {
    gap: 1rem;
    padding: 0.75rem;
  }

  .search-container {
    flex-direction: column;
    gap: 0.5rem;
  }

  .search-input {
    font-size: 0.95rem;
  }

  .search-btn {
    width: 100%;
  }

  .engine-switcher {
    gap: 1rem;
  }

  .engine-btn {
    padding: 0.5rem;
  }

  .engine-icon {
    width: 36px;
    height: 36px;
    font-size: 0.9rem;
  }

  .engine-name {
    font-size: 0.75rem;
  }

  .indicator {
    bottom: -28px;
  }

  .indicator-pill {
    width: 50px;
  }
}

/* ============ 深色模式支持 ============ */
@media (prefers-color-scheme: dark) {
  :root {
    --glass-bg: rgba(30, 30, 40, 0.7);
    --text-primary: #F3F4F6;
    --text-secondary: #D1D5DB;
    --text-muted: #9CA3AF;
  }

  .search-container {
    background: rgba(30, 30, 40, 0.7);
    border-color: rgba(255, 255, 255, 0.1);
  }

  .search-input {
    color: var(--text-primary);
  }

  .engine-switcher-wrapper {
    background: rgba(30, 30, 40, 0.5);
    border-color: rgba(255, 255, 255, 0.1);
  }
}
</style>
