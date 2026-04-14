<template>
  <div class="login-container">
    <div class="login-box">
      <h2>欢迎登录</h2>
      
      <div class="form-placeholder">
        </div>

      <div class="other-login-wrapper">
        <div class="divider">
          <span>其他登录方式</span>
        </div>
        
        <div class="logo-container">
          <div class="logo-item" title="游客登录" @click="handleLogin('guest')">
            <el-icon :size="24"><User /></el-icon>
          </div>
          <div class="logo-item" title="微信登录" @click="handleLogin('wechat')">
            <el-icon :size="24" color="#07C160"><ChatDotRound /></el-icon>
          </div>
          <div class="logo-item" title="GitHub登录" @click="handleLogin('github')">
            <el-icon :size="24"><Platform /></el-icon>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { User, ChatDotRound, Platform } from '@element-plus/icons-vue'

const handleLogin = (type) => {
  console.log('正在使用的登录方式:', type)
  if (type === 'guest') {
    alert('正在以游客身份进入...')
    // 这里可以写跳转首页的逻辑
  } else {
    alert(type + ' 登录功能正在对接 Flask 后端...')
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: #f5f7fa;
}

.login-box {
  width: 400px;
  padding: 40px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.other-login-wrapper {
  margin-top: 40px;
  position: relative;
  z-index: 10; /* 确保在最上层，解决无法点击问题 */
}

.divider {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  color: #999;
  font-size: 13px;
}
.divider::before, .divider::after {
  content: "";
  flex: 1;
  height: 1px;
  background: #ebeef5;
}
.divider span { padding: 0 15px; }

.logo-container {
  display: flex;
  justify-content: center;
  gap: 30px;
}

.logo-item {
  width: 46px;
  height: 46px;
  background: #f0f2f5;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  pointer-events: auto; /* 强制开启点击事件 */
}

.logo-item:hover {
  background: #e4e7ed;
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
</style>
